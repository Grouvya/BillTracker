#!/usr/bin/env python3
# Version 7.2.0 (Security & Georgian Localization)
# To run: pip install PyQt6 cryptography

__version__ = '7.2.0'

import sys
import os
import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from datetime import datetime, date, timedelta
import threading
import webbrowser
import urllib.request
import ssl
import ctypes
import hashlib
import shutil
import csv
import platform  # For cross-platform detection
import re  # For input sanitization and validation

# Platform-specific imports
if platform.system() == 'Windows':
    import winreg  # For Start with Windows (Windows only)
    import winsound # For audio notifications

import logging

# Configure logging
log_dir = os.path.join(os.path.expanduser('~'), '.bill_tracker')
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, 'app.log'),
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# ReportLab Imports
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox,
    QMessageBox, QDialog, QFormLayout, QDateEdit, QFileDialog, QProgressBar, QScrollArea, QListWidget,
    QListWidgetItem, QGroupBox, QGridLayout, QDoubleSpinBox, QInputDialog, QListWidgetItem as ListItem,
    QMenu, QAbstractItemView, QGraphicsDropShadowEffect, QGraphicsBlurEffect, QSystemTrayIcon, QTabWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QCalendarWidget, QSpinBox, QDialogButtonBox,
    QFrame, QStyle
)
from PyQt6.QtCore import Qt, QTimer, QDate, QThread, pyqtSignal, QPoint, QRectF, QRect
from PyQt6.QtGui import QFont, QColor, QAction, QIcon, QPalette, QPainter, QPen, QBrush, QTextDocument, QShortcut, QKeySequence, QPainterPath
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtNetwork import QLocalServer, QLocalSocket
from PyQt6.QtWidgets import QComboBox as _QComboBox

TRANSLATIONS = {
    'English': {
        "app_title": "Bill & Savings Tracker",
        "budget_group_title": "Set Your Budget",
        "budget_row_title": "Budget Amount",
        "set_budget_button": "Set Budget",
        "add_bill_group_title": "Add a New Bill",
        "bill_name_row": "Bill Name",
        "amount_row": "Amount",
        "due_date_row": "Due Date",
        "add_bill_button": "Add Bill",
        "summarize_in_label": "Summarize in:",
        "total_unpaid_label": "Total of Unpaid Bills:",
        "budget_after_paying_label": "Budget After Paying Bills:",
        "actions_group_title": "Actions",
        "converter_button": "Converter",
        "clear_data_button": "Clear Data",
        "btn_contact": "📩 Contact",
        "btn_donate": "💳 Donate",
        "refresh_rates_button": "Refresh Rates",
        "settings_button": "Settings",
        "unpaid_bills_title": "Unpaid Bills",
        "sort_name_button": "Search Currency",
        "sort_date_button": "Date",
        "sort_amount_button": "Amount",
        "paid_bills_title": "Paid Bills",
        "credits_label": "made with <3 by Grouvya!",
        "pay_button": "Pay",
        "due_on_label": "Due:",
        "no_date_label": "No Date",
        "edit_bill_title": "Edit Bill",
        "bill_name_label": "Bill Name",
        "amount_label": "Amount",
        "currency_label": "Currency",
        "due_date_label": "Due Date",
        "save_changes_button": "Save Changes",
        "converter_title": "Currency Converter",
        "from_label": "From",
        "to_label": "To",
        "convert_button": "Convert",
        "settings_title": "Settings",
        "data_file_group_title": "Data File Location",
        "browse_button": "Browse...",
        "dialog_input_error": "Input Error",
        "error_enter_name_amount": "Please enter both name and amount.",
        "error_positive_amount": "Please enter a valid positive amount.",
        "error_no_exchange_rate": "Could not find exchange rate.",
        "error_valid_number": "Please enter a valid number for the budget.",
        "info_budget_set": "Budget Set",
        "info_budget_set_to": "Budget set to {}",
        "info_path_saved": "Path Saved",
        "info_path_saved_msg": "Data file path has been updated.",
        "info_data_cleared": "Data Cleared",
        "info_data_cleared_msg": "All data has been cleared.",
        "dialog_confirm_payment": "Confirm Payment",
        "confirm_payment_msg": "Are you sure you want to pay '{}'?",
        "dialog_confirm_delete": "Confirm Delete",
        "confirm_delete_msg": "Are you sure you want to delete '{}'?",
        "dialog_clear_data": "Clear All Data",
        "confirm_clear_data_msg": "Are you sure you want to delete all bills and reset your budget?",
        "invalid_input": "Invalid Input",
        "api_error": "API error. Using cached rates.",
        "network_error": "Network error. Using cached rates.",
        "rates_updated_at": "Live rates updated: {}",
        "category_label": "Category",
        "repeat_label": "Repeat",
        "frequency_none": "No Repeat",
        "frequency_weekly": "Weekly",
        "frequency_monthly": "Monthly",
        "frequency_yearly": "Yearly",
        "tab_bills": "Bills",
        "tab_charts": "Charts",
        "tab_dashboard": "Dashboard",
        "tab_unpaid": "Unpaid Bills",
        "tab_paid": "Paid History",
        "chart_budget_title": "Budget vs Expenses",
        "chart_category_title": "Spending by Category",
        "lbl_yearly": "Yearly",
        "title_invalid_path": "Invalid Path",
        "msg_invalid_path_security": "For security reasons, data files must be stored in your user directory.\nSystem directories are not allowed.",
        "msg_csv_read_failed": "Failed to read CSV: {}",
        "title_permission_denied": "Permission Denied",
        "msg_admin_rights_required": "Administrator rights required to modify startup settings.",
        "notification_title": "Bills Due Soon",
        "notification_msg": "You have {} bills due today or tomorrow!",
        "lang_restart_msg": "Language changed. Please restart the application to apply changes.",
        "lang_group_title": "Language",
        "btn_mark_paid": "Mark Paid",
        "btn_view_details": "View Details",
        # New Translations
        "chk_start_windows": "Start with Windows",
        "chk_minimize_tray": "Minimize to Tray on Close",
        "btn_minimize_tray": "Minimize to Tray",
        "label_notify_me": "Notify me:",
        "suffix_days_advance": " days in advance",
        "btn_save_settings": "Save Settings",
        "group_backup_restore": "Backup & Restore",
        "btn_create_backup": "Create Backup",
        "btn_restore_selected": "Restore Selected",
        "group_danger_zone": "Danger Zone",
        "btn_clear_all_data": "🗑️ Clear All Data",
        "title_backup_created": "Backup Created",
        "msg_backup_created": "Manual backup created successfully.",
        "title_error": "Error",
        "msg_backup_failed": "Failed to create backup: {}",
        "title_selection_required": "Selection Required",
        "msg_select_backup": "Please select a backup to restore.",
        "title_confirm_restore": "Confirm Restore",
        "msg_confirm_restore": "Are you sure you want to restore '{}'?\nCurrent data will be overwritten.",
        "title_restored": "Restored",
        "msg_restored": "Data restored successfully.",
        "title_restore_failed": "Restore Failed",
        "msg_restore_error": "Error restoring backup: {}",
        "btn_delete_selected": "Delete Selected",
        "title_confirm_delete_backup": "Confirm Delete",
        "msg_confirm_delete_backup": "Are you sure you want to delete the backup '{}'?",
        "msg_backup_deleted": "Backup deleted successfully.",
        "title_clear_all_data": "Clear All Data",
        "msg_confirm_clear_1": "Are you sure you want to delete ALL data?\nThis action cannot be undone!",
        "title_double_confirm": "Double Confirmation",
        "msg_confirm_clear_2": "Really delete everything? All bills, budget, and settings will be lost.",
        "title_data_cleared": "Data Cleared",
        "msg_data_cleared_restart": "All data has been cleared.",
        "title_restart_required": "Restart Required",
        "btn_copy_result": "📋 Copy Result",
        "title_copied": "Copied",
        "msg_copied": "Result copied to clipboard!",
        "msg_running_background": "App is running in the background.",
        "label_monthly_history": "Monthly Spending History",
        "tab_trends": "📊 Trends",
        "tab_calendar": "📅 Calendar",
        "tab_about": "ℹ️ About",
        "title_quick_status": "Quick Status",
        "btn_export_csv": "📂 Export CSV",
        "btn_export_pdf": "📄 Export PDF",
        "title_save_report": "Save PDF Report",
        "msg_report_generated": "PDF Report generated successfully!",
        "msg_report_created": "Report saved to {}",
        "msg_report_failed": "Failed to generate PDF report. Check logs.",
        "group_support_data": "Support & Data",
        "group_quick_status": "Quick Status",
        "label_filter_category": "Filter by Category:",
        "item_all_categories": "All Categories",
        "header_name": "Name",
        "header_amount": "Amount",
        "header_category": "Category",
        "header_due_date": "Due Date",
        "header_frequency": "Frequency",
        "header_paid_date": "Paid Date",
        "label_calendar_hint": "Select a date to see bills.",
        "msg_no_backups": "No backups found.",
        "msg_bill_name_long": "Bill name is too long (max 100 chars).",
        "msg_amount_large": "Amount is too large.",
        "msg_invalid_format": "Invalid input format.",
        "msg_data_restored_reload": "Data restored successfully. Reloading...",
        "msg_data_tampered": "Data Integrity Violation!\n\nThe data file has been modified externally.\nThis could be due to tampering or corruption.\n\nDo you want to restore from the last automatic backup?",
        "title_invalid_pin": "Invalid PIN",
        "msg_pin_too_short": "PIN must be at least 4 digits.",
        "msg_pin_set_enabled": "PIN has been set and enabled.",
        "title_recurring_created": "Recurring Bill Created",
        "msg_recurring_created": "Next {} due on {}",
        "title_export_success": "Export Successful",
        "msg_export_success": "Data exported to {}",
        "title_export_failed": "Export Failed",
        "label_first_run_title": "Welcome to BillTracker!",
        "label_select_language": "Please select your preferred language:",
        "btn_start_app": "Start Application",
        "legend_save_image": "💾 Save Chart as Image",
        "title_save_chart": "Save Chart",
        "title_saved": "Saved",
        "msg_chart_saved": "Chart saved to {}",
        "btn_search": "🔍 Search",
        "title_select_currency": "Select Currency",
        "label_search_currency": "Search currency (code, symbol, or name):",
        "btn_ok": "OK",
        "btn_cancel": "Cancel",
        "label_remaining": "Remaining",
        "label_unpaid_bills_chart": "Unpaid Bills",
        "label_due_on": "Due on {}: {}",
        "label_no_bills_due": "No bills due on {}",
        "filter_csv": "CSV Files (*.csv)",
        "title_export_data": "Export Data",
        "categories_list": ["Housing", "Utilities", "Food", "Transport", "Subscription", "Debt", "Healthcare", "Personal", "Other"],
        "frequencies_list": ["No Repeat", "Weekly", "Monthly", "Yearly"],
        "label_filter_category": "Filter by Category:",
        "item_all_categories": "All Categories",
        "label_total_paid": "Total Paid",
        "menu_pay_bill": "💰 Pay Bill",
        "menu_edit_bill": "✏️ Edit Bill",
        "menu_delete_bill": "🗑️ Delete Bill",
        "menu_restore_unpaid": "↩️ Restore to Unpaid",
        "menu_delete_permanently": "🗑️ Delete Permanently",
        "title_confirm_delete_history": "Confirm Delete",
        "msg_confirm_delete_history": "Are you sure you want to delete '{}' from history?",
        "title_no_history": "No History",
        "msg_no_history": "No paid bills found.",
        "btn_contact": "📩 Contact",
        "btn_donate": "💳 Donate",
        "credits_link": "✨ Created by Grouvya! ✨",
        "btn_search": "🔍 Search Bills",
        "title_search": "Search Bills",
        "label_search_hint": "Search by name, amount, category, or date...",
        "header_status": "Status",
        "status_unpaid": "Unpaid",
        "status_paid": "Paid",
        "menu_view_details": "👁️ View Details",
        "msg_no_results": "No bills found matching your search.",
        "label_shortcut_search": "Press Ctrl+F to Search",
        "label_shortcut_add": "Press Ctrl+N to Add Bill",
        "title_success": "Success",
        "msg_bill_added": "Bill '{}' added successfully!",
        "title_manage_categories": "Manage Categories",
        "label_manage_categories_hint": "Manage your custom categories:",
        "placeholder_new_category": "New Category Name",
        "btn_add": "Add",
        "btn_remove": "Remove",
        "label_pin_unlock": "Enter PIN to unlock:",
        "label_pin_set_new": "Set new 4-6 digit PIN:",
        "btn_unlock": "Unlock",
        "label_confirm_pin": "Confirm PIN:",
        "placeholder_confirm_pin": "****",
        "label_pin_hint_setup": "PIN Hint (optional):",
        "placeholder_hint": "e.g., birthday, year...",
        "msg_pins_dont_match": "PINs do not match. Please try again.",
        "msg_pin_hint_prefix": "Hint: {}",
        "btn_save_pin": "Save PIN",
        "group_security_pin": "Security (PIN Protection)",
        "chk_enable_pin": "Enable PIN Protection",
        "btn_set_change_pin": "Set/Change PIN",
        # Auto-lock
        "chk_auto_lock": "Auto-lock on idle",
        "chk_lock_on_minimize": "Lock when minimized",
        "label_idle_timeout": "Lock after",
        "title_exit_min": "Exit or Minimize?",
        "msg_exit_min": "Do you want to minimize to tray or close the application?",
        "btn_minimize": "Minimize",
        "btn_exit": "Close App",
        "suffix_minutes": " minutes",
        "msg_app_locked": "Application Locked",
        "msg_enter_pin_unlock": "Enter your PIN to unlock",
        # Brute-force protection
        "msg_too_many_attempts": "Too many failed attempts!",
        "msg_locked_out_until": "Locked out until: {time}",
        "msg_attempts_remaining": "Attempts remaining: {count}",
        "btn_reset_app": "Reset App",
        "title_reset_app": "Reset Application",
        "msg_reset_warning": "⚠️ Factory Reset\n\nThis will DELETE ALL your bills, settings, and PIN.\n\nAre you sure?",
        "title_final_warning": "FINAL WARNING",
        "msg_final_warning": "This action cannot be undone.\n\nALL DATA WILL BE LOST PERMANENTLY.\n\nProceed?",
        "title_reset_complete": "Reset Complete",
        "msg_reset_complete": "Application has been reset.\nPlease restart the app.",
        "msg_reset_error": "Failed to reset: {}",
        "btn_factory_reset_full": "Factory Reset (Delete All Data & Configs)",
        "title_factory_reset": "Factory Reset",
        "title_confirm_reset": "Confirm Reset",
        "msg_reset_success_close": "Application reset successful.\nThe application will now close.",
        "msg_factory_reset_warning": "⚠️ You are about to DELETE ALL DATA.\n\nThis will remove:\n- All Bills\n- All Settings\n- PIN & Security\n- Backups\n\nThis cannot be undone.",
        "msg_type_delete": "Type 'DELETE' to confirm:",
        "title_export_error": "Export Error",
        "title_access_denied": "Access Denied",
        "msg_pin_fail_exit": "Incorrect PIN. Attempts remaining: {count}. App will close.",
        
        # Backup & Restore strings
        "group_backups": "Backups & Recovery",
        "lbl_backup_location": "Archive Location",
        "btn_backup_config": "Backup Config",
        "btn_backup_data": "Backup Data",
        "btn_restore_config": "Restore Config",
        "btn_restore_data": "Restore Data",
        "btn_reset_default": "Default",
        "msg_restore_warning": "Warning: This will overwrite your current data/settings. Continue?",
        "msg_restart_required": "Application restart required to apply changes.",
        "msg_backup_success": "Backup created successfully!",
        "title_backup_config": "Save Config Backup",
        "title_backup_data": "Save Data Backup",
        "title_restore_config": "Select Config to Restore",
        "title_restore_data": "Select Data to Restore",
        "msg_select_single_restore": "Please select only one backup to restore.",
        "msg_batch_delete_success": "{} backup(s) deleted successfully.",
        "msg_confirm_delete_backup_batch": "Are you sure you want to delete {} backups?",
        
        # Categories
        "msg_lockout_wait": "Account locked due to too many failed PIN attempts.\n\nLocked out until: {time}\n\nPlease try again later.",
        "msg_lockout_new": "Too many failed PIN attempts!\n\nAccount locked for 5 minutes.\n\nLocked out until: {time}",
        "msg_loading_config": "Loading configuration...",
        "msg_init_security": "Initializing security...",
        "msg_loading_rates": "Loading exchange rates...",
        "msg_prep_interface": "Preparing interface...",
        "msg_finalizing": "Finalizing...",
        "title_secure_access": "BillTracker - Secure Access",
        # v6.2.0 Strings
        "tab_notifications": "Notifications",
        "lbl_webhook_url": "Webhook URL (Discord/Slack/Telegram)",
        "lbl_reminder_time": "Daily Reminder Time",
        "btn_test_webhook": "Test Webhook",
        "msg_webhook_test_sent": "Test notification sent to webhook!",
        "msg_webhook_error": "Webhook failed: {}",
        "btn_switch_mini": "Mini Mode",
        "title_mini_mode": "Mini Tracker",
        "lbl_budget_rem": "Remaining Budget:",
        "lbl_due_today": "Due Today:",
        "lbl_overdue": "Overdue",
        "lbl_total_saved": "Total Saved:",
        "lbl_no_file_selected": "No file selected",
        "lbl_preview_top_5": "Preview (Top 5 lines):",
        "lbl_cloud_sync_desc": "App will automatically save an encrypted copy for syncing.",
        "btn_pick_color": "Pick Custom Color",
        "group_column_mapping": "Column Mapping",
        "group_general_settings": "General Settings",
        "group_aesthetics": "Aesthetics",
        "group_cloud_sync": "Cloud Sync",
        "title_language_selection": "Language Selection",
        "title_security_alert": "Security Alert",
        "btn_full_mode": "Full App",
        "group_notif_settings": "Notification Settings",
        "chk_enable_webhooks": "Enable Webhook Notifications",
        # v6.3.0 Strings
        "tab_subscriptions": "💳 Subscriptions",
        "btn_import_csv": "📥 Import Bank Statement",
        "lbl_burn_rate": "Monthly Burn Rate",
        "lbl_trend_30d": "30-Day Trend",
        "title_csv_import": "Import CSV",
        "msg_csv_mapped": "Mapped {} bills from CSV.",
        "msg_csv_invalid": "No valid transactions found in CSV.",
        "btn_select_csv": "Select CSV",
        "lbl_map_name": "Name Column",
        "lbl_map_amount": "Amount Column",
        "lbl_map_date": "Date Column",
        "chk_is_subscription": "Mark as Subscription",
        "tab_savings": "🎯 Savings",
        "lbl_yearly_burn": "Yearly Burn Rate",
        "lbl_days_until": "Days until payment",
        "lbl_savings_goals": "Savings Goals",
        "btn_add_goal": "Add Goal",
        "btn_add_savings": "Add Savings",
        "lbl_goal_name": "Goal Name",
        "lbl_target_amount": "Target Amount",
        "lbl_current_amount": "Current Amount",
        "tab_about": "ℹ️ About",
    },
    'Georgian': {
        "app_title": "ხარჯების და გადასახადების ტრეკერი",
        "budget_group_title": "ბიუჯეტის განსაზღვრა",
        "budget_row_title": "ბიუჯეტის რაოდენობა",
        "set_budget_button": "ბიუჯეტის შენახვა",
        "add_bill_group_title": "ახალი გადასახადის დამატება",
        "bill_name_row": "დასახელება",
        "amount_row": "თანხა",
        "due_date_row": "გადახდის თარიღი",
        "add_bill_button": "დამატება",
        "summarize_in_label": "ჯამური ვალუტა:",
        "total_unpaid_label": "სულ გადასახდელი:",
        "budget_after_paying_label": "დარჩენილი ბიუჯეტი:",
        "actions_group_title": "მოქმედებები",
        "converter_button": "კონვერტერი",
        "clear_data_button": "მონაცემების წაშლა",
        "btn_contact": "📩 კონტაქტი",
        "btn_donate": "💳 დონაცია",
        "refresh_rates_button": "კურსების განახლება",
        "settings_button": "პარამეტრები",
        "unpaid_bills_title": "გადასახდელი ბილეთები",
        "sort_name_button": "ვალუტის ძებნა",
        "sort_date_button": "თარიღი",
        "sort_amount_button": "თანხა",
        "paid_bills_title": "გადახდილი ისტორია",
        "credits_label": "შექმნილია <3 Grouvya-ს მიერ!",
        "pay_button": "გადახდა",
        "due_on_label": "ვადა:",
        "no_date_label": "უვადო",
        "edit_bill_title": "რედაქტირება",
        "bill_name_label": "დასახელება",
        "amount_label": "თანხა",
        "currency_label": "ვალუტა",
        "due_date_label": "ვადა",
        "save_changes_button": "შენახვა",
        "converter_title": "ვალუტის კონვერტერი",
        "from_label": "დან",
        "to_label": "ში",
        "convert_button": "კონვერტაცია",
        "settings_title": "პარამეტრები",
        "data_file_group_title": "მონაცემთა ფაილი",
        "browse_button": "არჩევა...",
        "dialog_input_error": "შეცდომა",
        "error_enter_name_amount": "გთხოვთ შეიყვანოთ სახელი და თანხა.",
        "error_positive_amount": "გთხოვთ შეიყვანოთ დადებითი თანხა.",
        "error_no_exchange_rate": "კურსი ვერ მოიძებნა.",
        "error_valid_number": "ბიუჯეტი უნდა იყოს რიცხვი.",
        "info_budget_set": "ბიუჯეტი შენახულია",
        "info_budget_set_to": "ბიუჯეტი განისაზღვრა: {}",
        "info_path_saved": "გზა შენახულია",
        "info_path_saved_msg": "მონაცემთა ფაილის მისამართი განახლდა.",
        "info_data_cleared": "მონაცემები წაიშალა",
        "info_data_cleared_msg": "ყველა მონაცემი წაშლილია.",
        "dialog_confirm_payment": "გადახდის დადასტურება",
        "confirm_payment_msg": "ნამდვილად გსურთ გადაიხადოთ '{}'?",
        "dialog_confirm_delete": "წაშლის დადასტურება",
        "confirm_delete_msg": "ნამდვილად გსურთ წაშალოთ '{}'?",
        "dialog_clear_data": "ყველაფრის წაშლა",
        "confirm_clear_data_msg": "ნამდვილად გსურთ წაშალოთ ყველა მონაცემი?",
        "invalid_input": "არასწორი მონაცემი",
        "api_error": "API შეცდომა. კურსები ქეშიდან.",
        "network_error": "ქსელის შეცდომა. კურსები ქეშიდან.",
        "rates_updated_at": "განახლდა: {}",
        "category_label": "კატეგორია",
        "repeat_label": "გამეორება",
        "frequency_none": "არ განმეორდეს",
        "frequency_weekly": "კვირაში ერთხელ",
        "frequency_monthly": "თვეში ერთხელ",
        "frequency_yearly": "წელიწადში ერთხელ",
        "tab_bills": "გადასახადები",
        "tab_charts": "გრაფიკები",
        "tab_dashboard": "დაფა",
        "tab_unpaid": "გადასახდელი",
        "tab_paid": "ისტორია",
        "chart_budget_title": "ბიუჯეტი vs ხარჯები",
        "chart_category_title": "ხარჯები კატეგორიების მიხედვით",
        "lbl_yearly": "წლიური",
        "title_invalid_path": "არასწორი მისამართი",
        "msg_invalid_path_security": "უსაფრთხოების მიზნით, ფაილები უნდა შეინახოს მომხმარებლის საქაღალდეში.\nსისტემური საქაღალდეები აკრძალულია.",
        "msg_csv_read_failed": "CSV-ს ჩატვირთვა ვერ მოხერხდა: {}",
        "title_permission_denied": "წვდომა აკრძალულია",
        "msg_admin_rights_required": "საჭიროა ადმინისტრატორის უფლებები პარამეტრების შესაცვლელად.",
        "notification_title": "მოახლოებული გადასახადები",
        "notification_msg": "თქვენ გაქვთ {} გადასახადი დღეს ან ხვალ!",
        "lang_restart_msg": "ენა შეიცვალა. ცვლილებების ასახვისთვის გთხოვთ გადატვირთოთ პროგრამა.",
        "lang_group_title": "ენა",
        # New Translations (Georgian)
        "chk_start_windows": "Windows-თან ერთად ჩართვა",
        "chk_minimize_tray": "ჩაკეცვა დახურვისას",
        "btn_minimize_tray": "სისტემურ ზონაში ჩაკეცვა",
        "label_notify_me": "შემატყობინე:",
        "suffix_days_advance": " დღით ადრე",
        "btn_save_settings": "პარამეტრების შენახვა",
        "group_backup_restore": "მონაცემთა არქივი",
        "btn_create_backup": "არქივის შექმნა",
        "btn_restore_selected": "არქივიდან აღდგენა",
        "group_danger_zone": "საშიში ზონა",
        "btn_clear_all_data": "🗑️ ყველაფრის წაშლა",
        "title_backup_created": "არქივი შეიქმნა",
        "msg_backup_created": "მონაცემთა არქივი წარმატებით შეიქმნა.",
        "title_error": "შეცდომა",
        "msg_backup_failed": "არქივის შექმნა ვერ მოხერხდა: {}",
        "title_selection_required": "აირჩიეთ ფაილი",
        "msg_select_backup": "გთხოვთ აირჩიოთ სარეზერვო ფაილი აღსადგენად.",
        "title_confirm_restore": "აღდგენის დადასტურება",
        "msg_confirm_restore": "ნამდვილად გსურთ აღადგინოთ '{}'?\nმიმდინარე მონაცემები გადაიწერება.",
        "title_restored": "აღდგენილია",
        "msg_restored": "მონაცემები წარმატებით აღდგა.",
        "title_restore_failed": "აღდგენა ვერ მოხერხდა",
        "msg_restore_error": "შეცდომა აღდგენისას: {}",
        "btn_delete_selected": "არჩეულის წაშლა",
        "title_confirm_delete_backup": "წაშლის დადასტურება",
        "msg_confirm_delete_backup": "ნამდვილად გსურთ წაშალოთ არქივი '{}'?",
        "msg_confirm_delete_backup_batch": "ნამდვილად გსურთ წაშალოთ {} არქივი?",
        "msg_backup_deleted": "არქივი წარმატებით წაიშალა.",
        "title_clear_all_data": "მონაცემების წაშლა",
        "msg_confirm_clear_1": "ნამდვილად გსურთ წაშალოთ ყველა მონაცემი?\nამ მოქმედების გაუქმება შეუძლებელია!",
        "title_double_confirm": "ორმაგი დადასტურება",
        "msg_confirm_clear_2": "ნამდვილად შლით ყველაფერს? ყველა მონაცემი დაიკარგება.",
        "title_data_cleared": "მონაცემები წაიშალა",
        "msg_data_cleared_restart": "ყველა მონაცემი წაშლილია.",
        "title_restart_required": "საჭიროა გადატვირთვა",
        "btn_copy_result": "📋 შედეგის კოპირება",
        "title_copied": "კოპირებულია",
        "msg_copied": "შედეგი დაკოპირდა ბუფერში!",
        "msg_running_background": "პროგრამა აგრძელებს მუშაობას ფონურ რეჟიმში.",
        "label_monthly_history": "თვის ხარჯების ისტორია",
        "tab_trends": "📊 ტრენდები",
        "tab_calendar": "📅 კალენდარი",
        "tab_about": "ℹ️ პროგრამის შესახებ",
        "title_quick_status": "სწრაფი სტატუსი",
        "btn_export_csv": "📂 CSV ექსპორტი",
        "btn_export_pdf": "📄 PDF ექსპორტი",
        "title_save_report": "PDF რეპორტის შენახვა",
        "msg_report_generated": "PDF რეპორტი წარმატებით შეიქმნა!",
        "msg_report_created": "რეპორტი შეინახა: {}",
        "msg_report_failed": "PDF რეპორტის შექმნა ვერ მოხერხდა.",
        "group_support_data": "მხარდაჭერა და მონაცემები",
        "group_quick_status": "სწრაფი სტატუსი",
        "label_filter_category": "ფილტრი კატეგორიით:",
        "item_all_categories": "ყველა კატეგორია",
        "header_name": "სახელი",
        "header_amount": "თანხა",
        "header_category": "კატეგორია",
        "header_due_date": "ვადა",
        "header_frequency": "სიხშირე",
        "header_paid_date": "გადახდის თარიღი",
        "label_calendar_hint": "აირჩიეთ თარიღი გადასახადების სანახავად.",
        "msg_no_backups": "არქივები ვერ მოიძებნა.",
        "msg_bill_name_long": "დასახელება ძალიან გრძელია (მაქს. 100 სიმბოლო).",
        "msg_amount_large": "თანხა ძალიან დიდია.",
        "msg_invalid_format": "არასწორი ფორმატი.",
        "msg_data_restored_reload": "მონაცემები აღდგენილია. ჩატვირთვა...",
        "msg_data_tampered": "მონაცემების ვერიფიკაცია ვერ მოხერხდა!\n\nფაილი გარედან არის შეცვლილი.\nგსურთ ბოლო არქივის აღდგენა?",
        "title_invalid_pin": "არასწორი PIN",
        "msg_pin_too_short": "PIN უნდა იყოს მინიმუმ 4 ციფრიანი.",
        "msg_pin_set_enabled": "PIN დაყენებული და გააქტიურებულია.",
        "title_recurring_created": "განმეორებადი გადასახადი შეიქმნა",
        "msg_recurring_created": "შემდეგი გადასახადი {} იქნება {} -ში",
        "title_export_success": "ექსპორტი წარმატებულია",
        "msg_export_success": "მონაცემები ექსპორტირებულია: {}",
        "title_export_failed": "ექსპორტი ვერ მოხერხდა",
        "label_first_run_title": "მოგესალმებათ BillTracker-ში!",
        "label_select_language": "გთხოვთ აირჩიოთ სასურველი ენა:",
        "btn_start_app": "პროგრამის გაშვება",
        "legend_save_image": "💾 შენახვა სურათად",
        "title_save_chart": "გრაფიკის შენახვა",
        "title_saved": "შენახულია",
        "msg_chart_saved": "გრაფიკი შენახულია: {}",
        "btn_search": "🔍 ძებნა",
        "title_select_currency": "აირჩიეთ ვალუტა",
        "label_search_currency": "მოძებნეთ ვალუტა (კოდი, სიმბოლო ან სახელი):",
        "btn_ok": "OK",
        "btn_cancel": "გაუქმება",
        "label_remaining": "დარჩენილი",
        "label_unpaid_bills_chart": "გადასახდელი",
        "label_due_on": "გადასახდელია {}: {}",
        "label_no_bills_due": "არ არის გადასახდელი {}-ში",
        "filter_csv": "CSV ფაილები (*.csv)",
        "title_export_data": "მონაცემების ექსპორტი",
        "categories_list": ["ბინა", "კომუნალურები", "საკვები", "ტრანსპორტი", "გამოწერები", "ვალები", "ჯანდაცვა", "პირადი", "სხვა"],
        "frequencies_list": ["არ განმეორდეს", "კვირეული", "თვიური", "წლიური"],
        "label_filter_category": "კატეგორიის ფილტრი:",
        "item_all_categories": "ყველა კატეგორია",
        "label_total_paid": "სულ გადახდილი",
        "menu_pay_bill": "💰 გადახდა",
        "menu_edit_bill": "✏️ რედაქტირება",
        "menu_delete_bill": "🗑️ წაშლა",
        "menu_restore_unpaid": "↩️ გადატანა გადასახდელში",
        "menu_delete_permanently": "🗑️ სამუდამოდ წაშლა",
        "title_confirm_delete_history": "წაშლის დადასტურება",
        "msg_confirm_delete_history": "ნამდვილად გსურთ '{}'-ს წაშლა ისტორიიდან?",
        "title_no_history": "ისტორია ცარიელია",
        "msg_no_history": "გადახდილი გადასახადები ვერ მოიძებნა.",
        "btn_contact": "📩 კონტაქტი",
        "btn_donate": "💳 დონაცია",
        "credits_link": "✨ შექმნილია Grouvya-ს მიერ! ✨",
        "btn_search": "🔍 ძებნა",
        "title_search": "გადასახადების ძებნა",
        "label_search_hint": "მოძებნეთ სახელით, თანხით, კატეგორიით ან თარიღით...",
        "header_status": "სტატუსი",
        "status_unpaid": "გადასახდელი",
        "status_paid": "გადახდილი",
        "menu_view_details": "👁️ დეტალები",
        "msg_no_results": "არ მოიძებნა შესაბამისი გადასახადი.",
        "label_shortcut_search": "დააჭირეთ Ctrl+F ძებნისთვის",
        "label_shortcut_add": "დააჭირეთ Ctrl+N დასამატებლად",
        "title_success": "წარმატება",
        "msg_bill_added": "გადასახადი '{}' წარმატებით დაემატა!",
        "title_manage_categories": "კატეგორიების მართვა",
        "label_manage_categories_hint": "მართეთ თქვენი პერსონალური კატეგორიები:",
        "placeholder_new_category": "ახალი კატეგორიის სახელი",
        "btn_add": "დამატება",
        "btn_remove": "წაშლა",
        "label_pin_unlock": "PIN კოდის შეყვანა:",
        "label_pin_set_new": "შეიყვანეთ ახალი 4-6 ციფრიანი PIN:",
        "label_confirm_pin": "დაადასტურეთ PIN:",
        "placeholder_confirm_pin": "****",
        "label_pin_hint_setup": "PIN მინიშნება (არასავალდებულო):",
        "placeholder_hint": "მაგ: დაბადების წელი...",
        "msg_pins_dont_match": "PIN კოდები არ ემთხვევა. სცადეთ თავიდან.",
        "msg_pin_hint_prefix": "მინიშნება: {}",
        "btn_unlock": "განბლოკვა",
        "btn_save_pin": "PIN-ის შენახვა",
        "group_security_pin": "უსაფრთხოება (PIN დაცვა)",
        "chk_enable_pin": "PIN დაცვის ჩართვა",
        "btn_set_change_pin": "PIN-ის დაყენება/შეცვლა",
        # Auto-lock
        "chk_auto_lock": "ავტომატური ბლოკირება უმოქმედობისას",
        "chk_lock_on_minimize": "დაბლოკვა ჩაკეცვისას",
        "label_idle_timeout": "დაბლოკვა შემდეგ",
        "title_exit_min": "გასვლა თუ ჩაკეცვა?",
        "msg_exit_min": "გსურთ აპლიკაციის ჩაკეცვა თუ დახურვა?",
        "btn_minimize": "ჩაკეცვა",
        "btn_exit": "დახურვა",
        "suffix_minutes": " წუთის შემდეგ",
        "msg_app_locked": "აპლიკაცია დაბლოკილია",
        "msg_enter_pin_unlock": "შეიყვანეთ PIN განსაბლოკად",
        # Brute-force protection
        "msg_too_many_attempts": "ძალიან ბევრი წარუმატებელი მცდელობა!",
        "msg_locked_out_until": "დაბლოკილია შემდეგ დრომდე: {time}",
        "msg_attempts_remaining": "დარჩენილი მცდელობები: {count}",
        "btn_reset_app": "აპლიკაციის განულება",
        "title_reset_app": "აპლიკაციის განულება",
        "msg_reset_warning": "⚠️ ქარხნული პარამეტრები\n\nეს წაშლის ყველა გადასახადს, პარამეტრს და PIN კოდს.\n\nდარწმუნებული ხართ?",
        "title_final_warning": "საბოლოო გაფრთხილება",
        "msg_final_warning": "ამ მოქმედების გაუქმება შეუძლებელია.\n\nყველა მონაცემი სამუდამოდ დაიკარგება.\n\nგსურთ გაგრძელება?",
        "title_reset_complete": "განულება დასრულდა",
        "msg_reset_complete": "აპლიკაცია განულდა.\nგთხოვთ გადატვირთოთ პროგრამა.",
        "msg_reset_error": "განულება ვერ მოხერხდა: {}",
        "btn_factory_reset_full": "ქარხნული პარამეტრები (ყველა მონაცემის წაშლა)",
        "btn_mark_paid": "გადახდა",
        "btn_view_details": "დეტალები",
        "title_factory_reset": "ქარხნული პარამეტრები",
        "title_confirm_reset": "განულების დადასტურება",
        "msg_reset_success_close": "განულება წარმატებით დასრულდა.\nაპლიკაცია დაიხურება.",
        "msg_factory_reset_warning": "⚠️ თქვენ აპირებთ ყველა მონაცემის წაშლას.\n\nწაიშლება:\n- ყველა გადასახადი\n- ყველა პარამეტრი\n- PIN და დაცვა\n- არქივები\n\nამ მოქმედების გაუქმება შეუძლებელია.",
        "msg_type_delete": "აკრიფეთ 'DELETE' დასადასტურებლად:",
        "title_export_error": "ექსპორტის შეცდომა",
        "title_access_denied": "წვდომა აკრძალულია",
        "msg_pin_fail_exit": "PIN არასწორია. დარჩენილი ცდები: {count}. აპლიკაცია დაიხურება.",

        # Backup & Restore strings
        "group_backups": "სარეზერვო ასლები & აღდგენა",
        "lbl_backup_location": "არქივის მდებარეობა",
        "btn_backup_config": "პარამეტრების შენახვა",
        "btn_backup_data": "მონაცემების შენახვა",
        "btn_restore_config": "პარამეტრების აღდგენა",
        "btn_restore_data": "მონაცემების აღდგენა",
        "btn_reset_default": "ნაგულისხმევი",
        "msg_restore_warning": "გაფრთხილება: ეს მოქმედება წაშლის მიმდინარე მონაცემებს. გსურთ გაგრძელება?",
        "msg_restart_required": "ცვლილებების ასახვისთვის საჭიროა პროგრამის გადატვირთვა.",
        "msg_backup_success": "სარეზერვო ასლი წარმატებით შეიქმნა!",
        "title_backup_config": "პარამეტრების ასლის შენახვა",
        "title_backup_data": "მონაცემების ასლის შენახვა",
        "title_restore_config": "აირჩიეთ აღსადგენი ფაილი",
        "title_restore_data": "აირჩიეთ აღსადგენი მონაცემები",

        # Categories
        "msg_lockout_wait": "ანგარიში დაბლოკილია.\n\nდაბლოკილია: {time}-მდე.\n\nგთხოვთ სცადოთ მოგვიანებით.",
        "msg_lockout_new": "ძალიან ბევრი წარუმატებელი მცდელობა!\n\nანგარიში დაბლოკილია 5 წუთით.\n\nდაბლოკილია: {time}-მდე.",
        "msg_loading_config": "კონფიგურაციის ჩატვირთვა...",
        "msg_init_security": "უსაფრთხოების ინიციალიზაცია...",
        "msg_loading_rates": "გაცვლითი კურსების ჩატვირთვა...",
        "msg_prep_interface": "ინტერფეისის მომზადება...",
        "msg_finalizing": "დასრულება...",
        "title_secure_access": "BillTracker - უსაფრთხო წვდომა",
        "msg_select_single_restore": "გთხოვთ აირჩიოთ მხოლოდ ერთი არქივი.",
        "msg_batch_delete_success": "{} არქივი წარმატებით წაიშალა.",
        "msg_confirm_batch_delete": "დარწმუნებული ხართ რომ გსურთ {} არქივის წაშლა?",
        # v6.2.0 Strings
        "tab_notifications": "შეტყობინებები",
        "lbl_webhook_url": "Webhook-ის მისამართი (Discord/Slack/Telegram)",
        "lbl_reminder_time": "ყოველდღიური შეხსენება",
        "btn_test_webhook": "ტესტირება",
        "msg_webhook_test_sent": "სატესტო შეტყობინება გაიგზავნა!",
        "msg_webhook_error": "შეტყობინება ვერ გაიგზავნ: {}",
        "btn_switch_mini": "მინი რეჟიმი",
        "title_mini_mode": "მინი ტრეკერი",
        "lbl_budget_rem": "დარჩენილი ბიუჯეტი:",
        "lbl_due_today": "დღეს გადასახდელი:",
        "lbl_overdue": "ვადაგადაცილებული",
        "lbl_total_saved": "სულ დაზოგილი:",
        "lbl_no_file_selected": "ფაილი არ არის არჩეული",
        "lbl_preview_top_5": "გადახედვა (ზედა 5 ხაზი):",
        "lbl_cloud_sync_desc": "აპლიკაცია ავტომატურად შეინახავს დაშიფრულ ასლს სინქრონიზაციისთვის.",
        "btn_pick_color": "ფერის არჩევა",
        "group_column_mapping": "სვეტების შესაბამისობა",
        "group_general_settings": "ზოგადი პარამეტრები",
        "group_aesthetics": "ვიზუალი",
        "group_cloud_sync": "ღრუბლოვანი სინქრონიზაცია",
        "title_language_selection": "ენის არჩევა",
        "title_security_alert": "უსაფრთხოების გაფრთხილება",
        "btn_full_mode": "აპლიკაცია",
        "group_notif_settings": "შეტყობინებების პარამეტრები",
        "chk_enable_webhooks": "Webhook შეტყობინებების ჩართვა",
        # v6.3.0 Strings (Georgian)
        "tab_subscriptions": "💳 გამოწერები",
        "btn_import_csv": "📥 ბანკის ამონაწერის იმპორტი",
        "lbl_burn_rate": "ყოველთვიური დახარჯვა",
        "lbl_trend_30d": "30-დღიანი ტრენდი",
        "title_csv_import": "CSV იმპორტი",
        "msg_csv_mapped": "იმპორტირებულია {} გადასახადი.",
        "msg_csv_invalid": "CSV-ში ვალიდური მონაცემები ვერ მოიძებნა.",
        "btn_select_csv": "აირჩიეთ CSV",
        "lbl_map_name": "სახელის სვეტი",
        "lbl_map_amount": "თანხის სვეტი",
        "lbl_map_date": "თარიღის სვეტი",
        "chk_is_subscription": "მონიშნე როგორც გამოწერა",
        "tab_savings": "🎯 დანაზოგები",
        "lbl_yearly_burn": "წლიური ხარჯი",
        "lbl_days_until": "გადახდამდე დარჩენილია",
        "lbl_savings_goals": "დაგროვების მიზნები",
        "btn_add_goal": "მიზნის დამატება",
        "btn_add_savings": "შენატანი",
        "lbl_goal_name": "მიზნის სახელი",
        "lbl_target_amount": "გეგმა",
        "lbl_current_amount": "ამჟამად",
        "tab_about": "ℹ️ შესახებ",
    }
}

class SafeStrings:
    """Wrapper for translation dictionary that prevents KeyError crashes."""
    def __init__(self, language='English'):
        self.language = language
        self._data = TRANSLATIONS.get(language, TRANSLATIONS['English'])
        self._fallback = TRANSLATIONS['English']

    def __getitem__(self, key):
        if key in self._data:
            return self._data[key]
        if key in self._fallback:
            logging.warning(f"Translation key '{key}' missing in '{self.language}'. Using English fallback.")
            return self._fallback[key]
        logging.error(f"Translation key '{key}' completely missing!")
        return f"[{key}]"

    def get(self, key, default=None):
        try:
            return self[key]
        except Exception:
            return default or f"[{key}]"



def strict_float(value):
    """Convert value to float, handling comma/dot and other common issues."""
    if isinstance(value, (int, float)):
        return float(value)
    if not value or not isinstance(value, str):
        return 0.0
    try:
        # Standardize decimal separator
        clean_val = value.replace(',', '.').strip()
        # Remove currency symbols if any sneak in
        clean_val = re.sub(r'[^\d.-]', '', clean_val)
        return float(clean_val)
    except (ValueError, TypeError):
        return 0.0

# Determine Language on Startup
STRINGS = SafeStrings('English')

# Global Constants based on STRINGS
# These are used for UI display
CATEGORIES = STRINGS["categories_list"]
FREQUENCIES = STRINGS["frequencies_list"]

# Canonical Keys for Internal Storage (Always English)
CANONICAL_CATEGORIES = TRANSLATIONS['English']['categories_list']
CANONICAL_FREQUENCIES = TRANSLATIONS['English']['frequencies_list']

def get_canonical_category(display_text):
    """Convert display text (any language) to canonical English key."""
    # Check if already canonical
    if display_text in CANONICAL_CATEGORIES:
        return display_text
    
    # Check all languages
    for lang_code, strings in TRANSLATIONS.items():
        if 'categories_list' in strings:
            try:
                idx = strings['categories_list'].index(display_text)
                return CANONICAL_CATEGORIES[idx]
            except ValueError:
                continue
    return display_text # Fallback

def get_canonical_frequency(display_text):
    """Convert display text (any language) to canonical English key."""
    # Check if already canonical
    if display_text in CANONICAL_FREQUENCIES:
        return display_text
        
    # Check all languages
    for lang_code, strings in TRANSLATIONS.items():
        if 'frequencies_list' in strings:
            try:
                idx = strings['frequencies_list'].index(display_text)
                return CANONICAL_FREQUENCIES[idx]
            except ValueError:
                continue
    return display_text # Fallback

def get_display_category(canonical_key):
    """Convert canonical key to current language display text."""
    try:
        idx = CANONICAL_CATEGORIES.index(canonical_key)
        return STRINGS["categories_list"][idx]
    except (ValueError, IndexError):
        return canonical_key

def get_display_frequency(canonical_key):
    """Convert canonical key to current language display text."""
    try:
        idx = CANONICAL_FREQUENCIES.index(canonical_key)
        return STRINGS["frequencies_list"][idx]
    except (ValueError, IndexError):
        return canonical_key

CURRENCY_FULL_NAMES = {
    'AFN': 'Afghan Afghani', 'ALL': 'Albanian Lek', 'AMD': 'Armenian Dram', 'ANG': 'Netherlands Antillean Guilder',
    'AOA': 'Angolan Kwanza', 'ARS': 'Argentine Peso', 'AUD': 'Australian Dollar', 'AWG': 'Aruban Florin',
    'AZN': 'Azerbaijani Manat', 'BAM': 'Bosnia-Herzegovina Convertible Mark', 'BBD': 'Barbadian Dollar', 'BDT': 'Bangladeshi Taka',
    'BGN': 'Bulgarian Lev', 'BHD': 'Bahraini Dinar', 'BIF': 'Burundian Franc', 'BMD': 'Bermudian Dollar',
    'BND': 'Brunei Dollar', 'BOB': 'Bolivian Boliviano', 'BRL': 'Brazilian Real', 'BSD': 'Bahamian Dollar',
    'BTN': 'Bhutanese Ngultrum', 'BWP': 'Botswana Pula', 'BYN': 'Belarusian Ruble', 'BZD': 'Belize Dollar',
    'CAD': 'Canadian Dollar', 'CDF': 'Congolese Franc', 'CHF': 'Swiss Franc', 'CLP': 'Chilean Peso',
    'CNY': 'Chinese Yuan', 'COP': 'Colombian Peso', 'CRC': 'Costa Rican Colón', 'CUP': 'Cuban Peso',
    'CVE': 'Cape Verdean Escudo', 'CZK': 'Czech Koruna', 'DJF': 'Djiboutian Franc', 'DKK': 'Danish Krone',
    'DOP': 'Dominican Peso', 'DZD': 'Algerian Dinar', 'EGP': 'Egyptian Pound', 'ERN': 'Eritrean Nakfa',
    'ETB': 'Ethiopian Birr', 'EUR': 'Euro', 'FJD': 'Fijian Dollar', 'FKP': 'Falkland Islands Pound',
    'GBP': 'British Pound Sterling', 'GEL': 'Georgian Lari', 'GHS': 'Ghanaian Cedi', 'GIP': 'Gibraltar Pound',
    'GMD': 'Gambian Dalasi', 'GNF': 'Guinean Franc', 'GTQ': 'Guatemalan Quetzal', 'GYD': 'Guyanese Dollar',
    'HKD': 'Hong Kong Dollar', 'HNL': 'Honduran Lempira', 'HRK': 'Croatian Kuna', 'HTG': 'Haitian Gourde',
    'HUF': 'Hungarian Forint', 'IDR': 'Indonesian Rupiah', 'ILS': 'Israeli New Shekel', 'INR': 'Indian Rupee',
    'IQD': 'Iraqi Dinar', 'IRR': 'Iranian Rial', 'ISK': 'Icelandic Króna', 'JEP': 'Jersey Pound',
    'JMD': 'Jamaican Dollar', 'JOD': 'Jordanian Dinar', 'JPY': 'Japanese Yen', 'KES': 'Kenyan Shilling',
    'KGS': 'Kyrgyzstani Som', 'KHR': 'Cambodian Riel', 'KMF': 'Comorian Franc', 'KPW': 'North Korean Won',
    'KRW': 'South Korean Won', 'KWD': 'Kuwaiti Dinar', 'KYD': 'Cayman Islands Dollar', 'KZT': 'Kazakhstani Tenge',
    'LAK': 'Lao Kip', 'LBP': 'Lebanese Pound', 'LKR': 'Sri Lankan Rupee', 'LRD': 'Liberian Dollar',
    'LSL': 'Lesotho Loti', 'LTL': 'Lithuanian Litas (historic)', 'LVL': 'Latvian Lats (historic)', 'LYD': 'Libyan Dinar',
    'MAD': 'Moroccan Dirham', 'MDL': 'Moldovan Leu', 'MGA': 'Malagasy Ariary', 'MKD': 'Macedonian Denar',
    'MMK': 'Myanmar Kyat', 'MNT': 'Mongolian Tögrög', 'MOP': 'Macanese Pataca', 'MRO': 'Mauritanian Ouguiya (historic)',
    'MUR': 'Mauritian Rupee', 'MVR': 'Maldivian Rufiyaa', 'MWK': 'Malawian Kwacha', 'MXN': 'Mexican Peso',
    'MYR': 'Malaysian Ringgit', 'MZN': 'Mozambican Metical', 'NAD': 'Namibian Dollar', 'NGN': 'Nigerian Naira',
    'NIO': 'Nicaraguan Córdoba', 'NOK': 'Norwegian Krone', 'NPR': 'Nepalese Rupee', 'NZD': 'New Zealand Dollar',
    'OMR': 'Omani Rial', 'PAB': 'Panamanian Balboa', 'PEN': 'Peruvian Sol', 'PGK': 'Papua New Guinean Kina',
    'PHP': 'Philippine Peso', 'PKR': 'Pakistani Rupee', 'PLN': 'Polish Złoty', 'PYG': 'Paraguayan Guaraní',
    'QAR': 'Qatari Riyal', 'RON': 'Romanian Leu', 'RSD': 'Serbian Dinar', 'RUB': 'Russian Ruble',
    'RWF': 'Rwandan Franc', 'SAR': 'Saudi Riyal', 'SBD': 'Solomon Islands Dollar', 'SCR': 'Seychellois Rupee',
    'SDG': 'Sudanese Pound', 'SEK': 'Swedish Krona', 'SGD': 'Singapore Dollar', 'SHP': 'Saint Helena Pound',
    'SLL': 'Sierra Leonean Leone', 'SOS': 'Somali Shilling', 'SRD': 'Surinamese Dollar', 'STD': 'Sao Tome Dobra (historic)',
    'SVC': 'Salvadoran Colón', 'SYP': 'Syrian Pound', 'SZL': 'Swazi Lilangeni', 'THB': 'Thai Baht',
    'TJS': 'Tajikistani Somoni', 'TMT': 'Turkmenistan Manat', 'TND': 'Tunisian Dinar', 'TOP': 'Tongan Paʻanga',
    'TRY': 'Turkish Lira', 'TTD': 'Trinidad and Tobago Dollar', 'TWD': 'New Taiwan Dollar', 'TZS': 'Tanzanian Shilling',
    'UAH': 'Ukrainian Hryvnia', 'UGX': 'Ugandan Shilling', 'USD': 'United States Dollar', 'UYU': 'Uruguayan Peso',
    'UZS': 'Uzbekistan Som', 'VEF': 'Venezuelan Bolívar (historic)', 'VND': 'Vietnamese Đồng', 'VUV': 'Vanuatu Vatu',
    'WST': 'Samoan Tala', 'XAF': 'Central African CFA Franc', 'XCD': 'East Caribbean Dollar', 'XOF': 'West African CFA Franc',
    'XPF': 'CFP Franc', 'YER': 'Yemeni Rial', 'ZAR': 'South African Rand', 'ZMW': 'Zambian Kwacha', 'ZWL': 'Zimbabwean Dollar'
}



def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Robust fallback: use script directory
        base_path = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_icon_path():
    """Get platform-appropriate main window icon path."""
    if platform.system() == 'Windows':
        return resource_path('billtracker.ico')
    else:
        return resource_path('billtracker.png')

def get_tray_icon_path():
    """Get platform-appropriate tray icon path."""
    tray_ico = resource_path('tray.ico')
    if os.path.exists(tray_ico):
        return tray_ico
    return get_icon_path()





def safe_parse_date(date_str, fallback='9999-12-31'):
    """Safely parse a date string, returning a fallback on failure."""
    if not date_str:
        return fallback
    try:
        # Check basic format to avoid expensive exception
        if len(date_str) != 10 or date_str[4] != '-' or date_str[7] != '-':
             raise ValueError
        datetime.strptime(date_str, '%Y-%m-%d')
        return date_str
    except (ValueError, TypeError):
        logging.warning(f"Invalid date encountered: {date_str}")
        return fallback

# Security Utilities - consolidated in v5.9.7 🛡️
def sanitize_input(text, max_length=100):
    """Strip potentially dangerous or invisible characters."""
    if not isinstance(text, str):
        return ""
    # Remove control characters and limit length
    cleaned = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)
    return cleaned[:max_length].strip()

def validate_file_path(path):
    """Validate file path to prevent traversal attacks."""
    try:
        # Resolve to absolute path
        abs_path = os.path.abspath(path)
        
        # Check if within user's home directory
        home = os.path.expanduser('~')
        if not abs_path.startswith(home):
            return False
            
        # Prevent access to system directories
        forbidden = ['system32', 'windows', 'program files']
        path_lower = abs_path.lower()
        if any(f in path_lower for f in forbidden):
            return False
            
        return True
    except:
        return False


class DataManager:
    """Handles loading and saving of config and application data."""
    def __init__(self, config_dir):
        self.config_dir = config_dir
        self.config_file = os.path.join(self.config_dir, 'config.json')
        self.data_file = os.path.join(self.config_dir, 'bill_data.json')
        self.security_file = os.path.join(self.config_dir, 'security.json')
        
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Load security metadata (Salt, PIN Hash, Lockout)
        self.security = self.load_security()
        
        self.encryption_salt = self.security.get('salt')
        if not self.encryption_salt:
            # MIGRATION: Check if we have salt in old config (v5.14.0 and older)
            # This is critical to avoid data loss (cannot decrypt data without original salt)
            migrated = False
            try:
                # We try to load config. If it's unencrypted (legacy), we can read it.
                legacy_config = {}
                if os.path.exists(self.config_file):
                    with open(self.config_file, 'r', encoding='utf-8') as f:
                        # Try plain load (legacy config is plain JSON)
                        try:
                            legacy_config = json.load(f)
                        except json.JSONDecodeError:
                            logging.debug("Old config.json not found or not legacy JSON.")
                
                if legacy_config.get('encryption_salt'):
                    self.encryption_salt = legacy_config['encryption_salt']
                    self.security['salt'] = self.encryption_salt
                    
                    # Also migrate PIN settings if present
                    if 'pin_hash' in legacy_config:
                        self.security['pin_hash'] = legacy_config['pin_hash']
                        self.security['pin_enabled'] = legacy_config.get('pin_enabled', False)
                    
                    self.save_security()
                    migrated = True
                    logging.info("Migrated security settings from config.json to security.json")
            except Exception as e:
                logging.error(f"Migration check failed: {e}")

            if not self.encryption_salt:
                # New Install or failed migration
                self.encryption_salt = base64.b64encode(os.urandom(16)).decode('utf-8')
                self.security['salt'] = self.encryption_salt
                self.save_security()

        try:
            # We don't have PIN yet, so this might return empty if encrypted
            self.config = self.load_config() 
        except Exception as e:
            logging.debug(f"Initial config load (pre-PIN) skipped: {e}")
            self.config = {}
            
        self.sync_path = self.config.get('sync_path')

    def _get_fernet(self, pin=None):
        """Derive key from PIN or use fallback obfuscation key."""
        if pin:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=base64.b64decode(self.encryption_salt),
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(pin.encode()))
        else:
            # Fallback obfuscation key (stable but not as secure as PIN-derived)
            # This is used when PIN is not enabled for basic non-readability
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'static_salt_for_obfuscation',
                iterations=1000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(b"default_obfuscation_key"))
        return Fernet(key)

    def load_security(self):
        """Load security metadata from separate file (Obfuscated)."""
        if os.path.exists(self.security_file):
            try:
                with open(self.security_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Try to decrypt with app-level key (Obfuscation)
                try:
                    fernet = self._get_fernet(None) # Use fallback key
                    decrypted = fernet.decrypt(content.encode())
                    return json.loads(decrypted.decode('utf-8'))
                except Exception:
                    # Fallback: Try loading as plain JSON (Migration or legacy)
                    try:
                        return json.loads(content)
                    except:
                        return {}
            except (IOError, OSError):
                return {}
        return {}

    def save_security(self):
        """Save security metadata (Obfuscated)."""
        try:
            # Obfuscate security file using app-level key
            # This protects the PIN hash from being read in plain text
            json_str = json.dumps(self.security, indent=4)
            fernet = self._get_fernet(None) # Use fallback key
            encrypted = fernet.encrypt(json_str.encode('utf-8'))
            
            with open(self.security_file, 'w', encoding='utf-8') as f:
                f.write(encrypted.decode('utf-8'))
        except IOError as e:
            logging.error(f"Error saving security metadata: {e}")

    def load_config(self, pin=None):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Try to detect if config is encrypted
                try:
                    # First try as plain JSON
                    config = json.loads(content)
                except json.JSONDecodeError:
                    # If JSON decode fails, try decrypting
                    if pin:
                        try:
                            fernet = self._get_fernet(pin)
                            decrypted = fernet.decrypt(content.encode())
                            config = json.loads(decrypted.decode('utf-8'))
                        except Exception as e:
                            logging.error(f"Failed to decrypt config: {e}")
                            return {}
                    else:
                        return {}
                
                self.data_file = config.get('data_file_path', self.data_file)
                return config
            except (IOError, OSError) as e:
                logging.error(f"Error loading config: {e}")
                return {}
        return {}

    def save_config(self, config_data, pin=None):
        try:
            # Check if PIN is enabled in config
            should_encrypt = pin or config_data.get('pin_enabled', False)
            
            # SYNC LANGUAGE to security metadata (so we can read it before PIN unlock)
            if 'language' in config_data:
                if self.security.get('language') != config_data['language']:
                    self.security['language'] = config_data['language']
                    self.save_security()
            
            if should_encrypt and pin:
                # Encrypt config
                json_str = json.dumps(config_data, indent=4)
                fernet = self._get_fernet(pin)
                encrypted = fernet.encrypt(json_str.encode('utf-8'))
                
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    f.write(encrypted.decode('utf-8'))
            else:
                # Save as plain JSON
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(config_data, f, indent=4)
        except (IOError, OSError) as e:
            logging.error(f"Error saving config: {e}")

    def load_data(self, pin=None):
        if os.path.exists(self.data_file):
            try:
                # Security: Check file size (max 10MB to prevent DoS)
                file_size = os.path.getsize(self.data_file)
                if file_size > 10 * 1024 * 1024:
                    logging.error(f"Data file too large: {file_size} bytes (max 10MB)")
                    return {}
                
                with open(self.data_file, 'rb') as f:
                    raw_content = f.read(10 * 1024 * 1024)  # Max 10MB read
                
                if not raw_content:
                    logging.warning(f"Data file {self.data_file} is empty (0 bytes). Returning empty data.")
                    return {}

                # Decryption logic
                fernet = self._get_fernet(pin)
                try:
                    decrypted_bytes = fernet.decrypt(raw_content)
                    content = decrypted_bytes.decode('utf-8')
                except Exception as e:
                    # If decryption fails, maybe it's plain text or wrong PIN
                    # We try to see if it's valid JSON plain text
                    try:
                        content = raw_content.decode('utf-8')
                        json.loads(content) # Verify it's JSON
                    except:
                        logging.error(f"Failed to decrypt data and it is not valid plain JSON. File: {self.data_file}, Size: {len(raw_content)} bytes. Error: {e}")
                        return {}

                # Integrity Check (on decrypted content)
                hash_file = self.data_file + ".sha256"
                is_tampered = False
                if os.path.exists(hash_file):
                    try:
                        with open(hash_file, 'r', encoding='utf-8') as f:
                            saved_hash = f.read().strip()
                        current_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
                        if current_hash != saved_hash:
                            is_tampered = True
                            logging.warning("Data file integrity check failed - hash mismatch")
                    except (IOError, OSError) as e:
                        logging.warning(f"Could not verify data integrity: {e}")

                data = json.loads(content)
                if not isinstance(data, dict):
                    print(f"DEBUG: Data loaded from '{self.data_file}' is not a dict: {type(data)}", flush=True)
                    return {}
                    
                print(f"DEBUG: Data loaded successfully. Keys: {list(data.keys())}", flush=True)
                print(f"DEBUG: Raw Currency Data in File: Budget='{data.get('budget_currency')}', Bill='{data.get('bill_currency')}', Summary='{data.get('summary_currency')}'", flush=True)
                
                # Schema validation (rest of the logic remains same)
                safe_data = {}
                safe_data['budget'] = float(data.get('budget', 0.0))
                safe_data['unpaid_bills'] = [b for b in data.get('unpaid_bills', []) if isinstance(b, dict) and ('name' in b or 'amount' in b)]
                safe_data['paid_bills'] = [b for b in data.get('paid_bills', []) if isinstance(b, dict) and ('name' in b or 'amount' in b)]
                safe_data['budget_currency'] = str(data.get('budget_currency', '$ (USD)'))
                safe_data['bill_currency'] = str(data.get('bill_currency', '$ (USD)'))
                safe_data['summary_currency'] = str(data.get('summary_currency', '$ (USD)'))
                safe_data['custom_categories'] = data.get('custom_categories', [])
                safe_data['savings_goals'] = data.get('savings_goals', [])
                
                # MIGRATION: Normalize categories
                for bill in safe_data['unpaid_bills'] + safe_data['paid_bills']:
                    if 'category' in bill:
                        bill['category'] = get_canonical_category(bill['category'])
                    if 'repeat_freq' in bill:
                        bill['repeat_freq'] = get_canonical_frequency(bill['repeat_freq'])
                
                if is_tampered:
                    safe_data['__tampered__'] = True
                    
                return safe_data
            except json.JSONDecodeError as e:
                logging.error(f"JSON decode error in data file: {e}")
                return {}
            except (IOError, OSError) as e:
                logging.error(f"File I/O error loading data: {e}")
                return {}
            except ValueError as e:
                logging.error(f"Value error in data file: {e}")
                return {}
        return {}

    def save_data(self, data_to_save, pin=None):
        import time
        try:
            # Prepare data
            json_str = json.dumps(data_to_save, indent=4, ensure_ascii=False)
            
            # 1. Integrity: Calculate and Save Hash (on plain JSON)
            data_hash = hashlib.sha256(json_str.encode('utf-8')).hexdigest()
            hash_file = self.data_file + ".sha256"
            with open(hash_file, 'w', encoding='utf-8') as f:
                f.write(data_hash)

            # 2. Encryption
            fernet = self._get_fernet(pin)
            encrypted_data = fernet.encrypt(json_str.encode('utf-8'))

            # 3. Atomic Write with Retry (Hardened for Windows 🛠️)
            tmp_file = self.data_file + ".tmp"
            with open(tmp_file, 'wb') as f:
                f.write(encrypted_data)
            
            # Atomic swap with retries for "Permission Denied"
            retries = 3
            for i in range(retries):
                try:
                    if os.path.exists(self.data_file):
                        os.replace(tmp_file, self.data_file)
                    else:
                        os.rename(tmp_file, self.data_file)
                    break
                except PermissionError as e:
                    if i == retries - 1:
                        logging.error(f"Final attempt failed to save data (Permission Error): {e}")
                        raise
                    logging.warning(f"Save retry {i+1} due to permission error: {e}")
                    time.sleep(0.5) # Wait for antivirus/indexer to release handle
            
            # Backup after successful save
            self.backup_data()
            
            # Also save to sync path if enabled
            if self.sync_path and os.path.isdir(self.sync_path):
                try:
                    sync_file = os.path.join(self.sync_path, 'bill_data.json')
                    with open(sync_file, 'wb') as f: # Use wb for encrypted binary
                        f.write(encrypted_data)
                    logging.info(f"Data synced to {self.sync_path}")
                except Exception as e:
                    logging.error(f"Sync failed: {e}")
            
            return True
        except (IOError, OSError) as e:
            logging.exception(f"Error saving data: {e}")

    def backup_data(self):
        """Create a rotating backup of the data file."""
        if not os.path.exists(self.data_file):
            return
            
        try:
            # Use configured backup dir or default
            backup_dir = self.config.get('backup_dir')
            if not backup_dir:
                backup_dir = os.path.join(self.config_dir, 'backups')
            
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = os.path.join(backup_dir, f"bill_data_{timestamp}.json")
            
            shutil.copy2(self.data_file, backup_path)
            
            # Rotate: Keep last 5 (Per folder)
            backups = sorted([os.path.join(backup_dir, f) for f in os.listdir(backup_dir) if f.startswith('bill_data_')])
            while len(backups) > 5:
                os.remove(backups.pop(0))
        except Exception as e:
            logging.error(f"Backup failed: {e}")

    def backup_config(self, target_path, pin=None):
        """Backup configuration to specific target."""
        if not os.path.exists(self.config_file):
            return False
        try:
            shutil.copy2(self.config_file, target_path)
            return True
        except Exception as e:
             logging.error(f"Config backup failed: {e}")
             return False

    def restore_file(self, source_path, file_type='data'):
        """Restore file from source_path.
        file_type: 'data' or 'config'
        """
        try:
            target = self.data_file if file_type == 'data' else self.config_file
            
            # Simple integrity check before copy?
            with open(source_path, 'r', encoding='utf-8') as f:
                content = f.read(1024) # Read header
                # Basic check: JSON?
                # If encrypted, it might be weird chars, but decent JSON parsers might fail fast.
                # However, encrypted files are Base64 text.
                # Just copy.
                pass
            
            shutil.copy2(source_path, target)
            return True
        except Exception as e:
            logging.error(f"Restore failed: {e}")
            return False

    def save_rates_cache(self, rates_data):
        try:
            cache_file = os.path.join(self.config_dir, 'rates_cache.json')
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(rates_data, f, indent=2)
        except IOError:
            pass

    def load_rates_cache(self):
        """Load cached exchange rates from disk."""
        cache_file = os.path.join(self.config_dir, 'rates_cache.json')
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return None
        return None
    
    # Security: Persistent lockout tracking
    def save_lockout_state(self, failed_attempts, lockout_until):
        """Save lockout state to persist across app restarts."""
        lockout_file = os.path.join(self.config_dir, '.lockout')
        try:
            state = {
                'failed_attempts': failed_attempts,
                'lockout_until': lockout_until.isoformat() if lockout_until else None
            }
            with open(lockout_file, 'w', encoding='utf-8') as f:
                json.dump(state, f)
        except (IOError, OSError) as e:
            logging.error(f"Failed to save lockout state: {e}")
    
    def load_lockout_state(self):
        """Load lockout state from disk."""
        lockout_file = os.path.join(self.config_dir, '.lockout')
        if os.path.exists(lockout_file):
            try:
                with open(lockout_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                lockout_until = None
                if state.get('lockout_until'):
                    lockout_until = datetime.fromisoformat(state['lockout_until'])
                return state.get('failed_attempts', 0), lockout_until
            except (json.JSONDecodeError, IOError, ValueError) as e:
                logging.error(f"Failed to load lockout state: {e}")
                return 0, None
        return 0, None
    
    def clear_lockout_state(self):
        """Clear lockout state (called on successful PIN entry)."""
        lockout_file = os.path.join(self.config_dir, '.lockout')
        try:
            if os.path.exists(lockout_file):
                os.remove(lockout_file)
        except OSError as e:
            logging.error(f"Failed to clear lockout state: {e}")
    

class APIThread(QThread):
    """Background thread for fetching currency rates."""
    finished = pyqtSignal(dict)

    def run(self):
        primary_url = "https://api.exchangerate.host/latest?base=USD"
        fallback_url = "https://open.er-api.com/v6/latest/USD"
        
        try:
            ctx = ssl.create_default_context()
            with urllib.request.urlopen(primary_url, context=ctx, timeout=10) as response:
                if response.status == 200:
                    content = response.read().decode('utf-8')
                    data = json.loads(content)
                    if 'rates' in data and isinstance(data['rates'], dict) and data['rates']:
                        normalized = {'conversion_rates': data['rates'], 'base_code': data.get('base', 'USD')}
                        self.finished.emit({'status': 'success', 'data': normalized})
                        return
        except (urllib.error.URLError, json.JSONDecodeError, ssl.SSLError, TimeoutError) as e:
            logging.warning(f"Primary API request failed: {e}")

        # Fallback
        try:
            ctx = ssl.create_default_context()
            with urllib.request.urlopen(fallback_url, context=ctx, timeout=10) as response:
                if response.status == 200:
                    content = response.read().decode('utf-8')
                    data = json.loads(content)
                    if 'rates' in data and isinstance(data['rates'], dict) and data['rates']:
                        normalized = {'conversion_rates': data['rates'], 'base_code': data.get('base_code', 'USD')}
                        self.finished.emit({'status': 'success', 'data': normalized})
                        return
        except (urllib.error.URLError, json.JSONDecodeError, ssl.SSLError, TimeoutError) as e:
            logging.warning(f"Fallback API request failed: {e}")

        self.finished.emit({'status': 'error', 'message': STRINGS["network_error"]})


class HistoryAPIThread(QThread):
    """Background thread for fetching historical currency data (30 days)."""
    finished = pyqtSignal(list)

    def __init__(self, base_currency="USD", target_currency="EUR"):
        super().__init__()
        self.base = base_currency
        self.target = target_currency

    def run(self):
        # Frankfurter API - simple and no API key required for historical data
        end_date = date.today().strftime('%Y-%m-%d')
        start_date = (date.today() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        url = f"https://api.frankfurter.app/{start_date}..{end_date}?from={self.base}&to={self.target}"
        
        try:
            ctx = ssl.create_default_context()
            with urllib.request.urlopen(url, context=ctx, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    rates_dict = data.get('rates', {})
                    # Convert dict to ordered list of values
                    history = []
                    for d in sorted(rates_dict.keys()):
                        history.append(rates_dict[d].get(self.target, 0))
                    self.finished.emit(history)
                    return
        except Exception as e:
            logging.warning(f"History API failed: {e}")
        
        self.finished.emit([])

class SparklineWidget(QWidget):
    """A custom widget to display a simple line chart (sparkline)."""
    def __init__(self, color="#6200ea"):
        super().__init__()
        self.data = []
        self.color = color
        self.setFixedHeight(50)
        self.setMinimumWidth(100)

    def set_data(self, data):
        self.data = data
        self.update()

    def paintEvent(self, event):
        if not self.data or len(self.data) < 2:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        padding = 5
        w = self.width() - 2 * padding
        h = self.height() - 2 * padding
        
        min_val = min(self.data)
        max_val = max(self.data)
        range_val = max_val - min_val if max_val != min_val else 1
        
        # Draw path
        path = QPainterPath()
        step = w / (len(self.data) - 1)
        
        for i, val in enumerate(self.data):
            x = padding + (i * step)
            # Invert Y (0 is top)
            y = self.height() - padding - ((val - min_val) / range_val * h)
            if i == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)
        
        pen = QPen(QColor(self.color), 2)
        painter.setPen(pen)
        painter.drawPath(path)



CURRENCY_SYMBOLS = {
    'AED': 'د.إ', 'ARS': '$', 'AUD': 'A$', 'AZN': '₼', 'BOB': 'Bs.', 'BRL': 'R$',
    'CAD': 'C$', 'CHF': 'CHF', 'CNY': '¥', 'CRC': '₡', 'CZK': 'Kč', 'DJF': 'Fdj',
    'DKK': 'kr', 'DOP': 'RD$', 'ETB': 'Br', 'EUR': '€', 'GBP': '£', 'GEL': '₾',
    'GMD': 'D', 'HKD': 'HK$', 'HUF': 'Ft', 'IDR': 'Rp', 'ILS': '₪', 'INR': '₹',
    'IRR': '﷼', 'ISK': 'kr', 'JPY': '¥', 'KES': 'KSh', 'KRW': '₩', 'KWD': 'د.ك',
    'MXN': '$', 'MYR': 'RM', 'NGN': '₦', 'NOK': 'kr', 'NZD': 'NZ$', 'PEN': 'S/.',
    'PHP': '₱', 'PKR': '₨', 'PLN': 'zł', 'QAR': 'ر.ق', 'RON': 'lei', 'RUB': '₽',
    'SAR': '﷼', 'SEK': 'kr', 'SGD': 'S$', 'SLL': 'Le', 'THB': '฿', 'TRY': '₺',
    'TWD': 'NT$', 'USD': '$', 'VND': '₫', 'ZAR': 'R'
}


def get_currency_list():
    """Returns dictionary of currency display strings to their metadata (code, symbol)."""
    # Dynamic generation to ensure ALL currencies in CURRENCY_FULL_NAMES are supported
    currency_data = {}
    
    # Sort for consistent order in dropdowns (by full name for better UX)
    sorted_codes = sorted(CURRENCY_FULL_NAMES.keys(), key=lambda k: CURRENCY_FULL_NAMES[k])
    
    for code in sorted_codes:
        name = CURRENCY_FULL_NAMES.get(code, code)
        symbol = CURRENCY_SYMBOLS.get(code, code)
        
        # Display Format: "Symbol - Full Name" e.g. "₾ - Georgian Lari"
        if symbol == code:
             display_key = f"{name}"
        else:
             display_key = f"{symbol} - {name}"
            
        currency_data[display_key] = {'code': code, 'symbol': symbol}
        
    return currency_data




class ThemeManager:
    """Manages application themes and providing stylesheets."""
    def __init__(self):
        self.current_theme = 'Dark'
        self.accent_color = '#6200ea' # Deep Purple
        
        self.palettes = {
            'Dark': {
                'bg': '#1e1e2d',
                'surface': '#2d2d3d',
                'text': '#ffffff',
                'text_secondary': '#b0b0b0',
                'border': '#3d3d3d',
                'success': '#00c853',
                'danger': '#e63946',
                'warning': '#ffaa00'
            },
            'Light': {
                'bg': '#f5f5f5',
                'surface': '#ffffff',
                'text': '#000000',
                'text_secondary': '#5f6368',
                'border': '#e0e0e0',
                'success': '#2e7d32',
                'danger': '#d32f2f',
                'warning': '#f57c00'
            },
            'Neon Night': {
                'bg': '#0f0c29',
                'surface': '#1a1a2e',
                'text': '#e0e0e0',
                'text_secondary': '#9a9ae0',
                'border': '#302b63',
                'success': '#00ffcc',
                'danger': '#ff007f',
                'warning': '#ffea00'
            },
            'Nordic Forest': {
                'bg': '#2e3440',
                'surface': '#3b4252',
                'text': '#eceff4',
                'text_secondary': '#d8dee9',
                'border': '#4c566a',
                'success': '#a3be8c',
                'danger': '#bf616a',
                'warning': '#ebcb8b'
            },
            'Pride': {
                'bg': '#121212',
                'surface': '#1e1e1e',
                'text': '#ffffff',
                'text_secondary': '#A0A0A0',
                'border': '#732982',
                'success': '#008026',
                'danger': '#E40303',
                'warning': '#FFED00',
                'scrollbar_handle': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #E40303, stop:0.2 #FF8C00, stop:0.4 #FFED00, stop:0.6 #008026, stop:0.8 #24408E, stop:1.0 #732982)'
            },
            'Trans Pride': {
                'bg': '#1a1a2e',
                'surface': '#16213e',
                'text': '#ffffff',
                'text_secondary': '#5BCEFA',
                'border': '#F5A9B8',
                'success': '#5BCEFA',
                'danger': '#F5A9B8',
                'warning': '#fdfdfd',
                'scrollbar_handle': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #5BCEFA, stop:0.25 #F5A9B8, stop:0.5 #FFFFFF, stop:0.75 #F5A9B8, stop:1.0 #5BCEFA)'
            }
        }
    
    def get_palette(self):
        return self.palettes.get(self.current_theme, self.palettes['Dark'])

    def set_theme(self, theme_name):
        if theme_name in self.palettes:
            self.current_theme = theme_name
            
    def set_accent(self, color_hex):
        self.accent_color = color_hex
        
    def get_contrast_color(self, hex_color):
        """Calculate if black or white text should be used based on color luminance."""
        try:
            hex_color = hex_color.lstrip('#')
            if len(hex_color) == 3:
                hex_color = ''.join([c*2 for c in hex_color])
            r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
            # Relative luminance formula
            luminance = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
            return '#000000' if luminance > 0.5 else '#ffffff'
        except:
            return '#ffffff'

    def get_stylesheet(self):
        p = self.get_palette()
        accent = self.accent_color
        contrast = self.get_contrast_color(accent)
        
        return f"""
            QMainWindow, QDialog {{ background-color: {p['bg']}; color: {p['text']}; }}
            QWidget {{ background-color: {p['bg']}; color: {p['text']}; }}
            QLabel {{ color: {p['text']}; }}
            QLineEdit, QDateEdit, QComboBox {{
                background-color: {p['surface']};
                color: {p['text']};
                border: 1px solid {p['border']};
                padding: 5px;
                border-radius: 5px;
            }}
            QGroupBox {{
                border: 1px solid {p['border']};
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }}
            QGroupBox::title {{ subcontrol-origin: margin; left: 10px; padding: 0 5px; }}
            QPushButton {{
                background-color: {accent};
                color: {contrast};
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color:  {accent}; opacity: 0.9; }}
            QPushButton:pressed {{ background-color: {accent}; opacity: 0.8; }}
            QTabWidget::pane {{ border: 1px solid {p['border']}; }}
            QTabBar::tab {{
                background-color: {p['surface']};
                color: {p['text']};
                padding: 8px 12px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }}
            QTabBar::tab:selected {{
                background-color: {accent};
                color: {contrast};
            }}
            QHeaderView::section {{
                background-color: {p['surface']};
                color: {p['text']};
                padding: 4px;
                border: 1px solid {p['border']};
            }}
            QTableWidget {{
                gridline-color: {p['border']};
                selection-background-color: {accent};
                selection-color: {contrast};
                background-color: {p['surface']};
                color: {p['text']};
            }}
            QScrollBar:vertical {{
                border: none;
                background: {p['bg']};
                width: 20px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {p.get('scrollbar_handle', p['border'])};
                min-height: 20px;
                border-radius: 10px;
            }}
            QScrollBar:horizontal {{
                border: none;
                background: {p['bg']};
                height: 20px;
                margin: 0px;
            }}
            QScrollBar::handle:horizontal {{
                background: {p.get('scrollbar_handle', p['border']).replace('y2:1', 'x2:1').replace('x2:0', 'x1:0') if 'scrollbar_handle' in p else p['border']};
                min-width: 20px;
                border-radius: 10px;
            }}
            QListWidget {{
                background-color: {p['surface']};
                color: {p['text']};
                border: 1px solid {p['border']};
            }}
            /* Calendar Widget Styling */
            QCalendarWidget QToolButton {{
                color: {p['text']};
                background-color: transparent;
                icon-size: 16px;
            }}
            QCalendarWidget QMenu {{
                background-color: {p['surface']};
                color: {p['text']};
            }}
            QCalendarWidget QSpinBox {{
                background-color: {p['surface']};
                color: {p['text']};
                selection-background-color: {accent};
                selection-color: {contrast};
            }}
            QCalendarWidget QAbstractItemView:enabled {{
                background-color: {p['surface']};
                color: {p['text']};
                selection-background-color: {accent};
                selection-color: {contrast};
            }}
            #qt_calendar_navigationbar {{
                background-color: {p['surface']};
                border-bottom: 1px solid {p['border']};
            }}
        """

class LazyCombo(_QComboBox):
    """QComboBox that populates items lazily on first showPopup to speed startup."""
    def __init__(self, items_provider=None, pending_text=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._items_provider = items_provider
        self._populated = False
        
        # If we have pending text, likely we want to select it immediately if possible,
        # but to be truly lazy we might wait. However, for reliability, if we have a value,
        # we generally want the combo to reflect it.
        # But to allow lazy loading flexibility, we can store it.
        # BUT, if someone calls setCurrentText later, we MUST populate.
        
        if pending_text:
            self.ensure_populated()
            self.setCurrentText(pending_text)

    def ensure_populated(self):
        """Force population of items without showing popup."""
        if not self._populated and self._items_provider:
             # Prevent re-entry
            self._populated = True
            items = self._items_provider()
            if items:
                self.addItems(items)

    def showPopup(self):
        self.ensure_populated()
        super().showPopup()
        
    def setCurrentText(self, text):
        self.ensure_populated()
        # If the item doesn't exist in the list, add it (for search results)
        if text and self.findText(text) == -1:
            self.addItem(text)
        super().setCurrentText(text)
        
    def setCurrentIndex(self, index):
        self.ensure_populated()
        super().setCurrentIndex(index)


class ToastNotification(QDialog):
    """Beautiful, interactive floating notification in the bottom right corner."""
    def __init__(self, parent, bills, theme_manager):
        super().__init__(parent, Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.bills = bills
        self.theme_manager = theme_manager
        self.setFixedWidth(350)
        
        # Apply current theme
        self.setStyleSheet(self.theme_manager.get_stylesheet())
        p = self.theme_manager.get_palette()
        accent = self.theme_manager.accent_color
        
        self.main_frame = QFrame(self)
        self.main_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {p['surface']};
                border: 2px solid {accent};
                border-radius: 10px;
            }}
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        content_layout = QVBoxLayout(self.main_frame)
        
        # Header
        header = QHBoxLayout()
        header.setContentsMargins(5, 5, 5, 5)
        title_lbl = QLabel("🔔 " + STRINGS["notification_title"])
        title_lbl.setStyleSheet("font-weight: bold; font-size: 13pt; color: white;")
        header.addWidget(title_lbl)
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(24, 24)
        close_btn.setStyleSheet(f"background: transparent; color: {p['text_secondary']}; font-weight: bold;")
        close_btn.clicked.connect(self.close)
        header.addWidget(close_btn)
        content_layout.addLayout(header)
        
        # Bills List
        bills_scroll = QScrollArea()
        bills_scroll.setWidgetResizable(True)
        bills_scroll.setMaximumHeight(200)
        bills_scroll.setStyleSheet("border: none; background: transparent;")
        
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        container_layout = QVBoxLayout(container)
        
        for bill in self.bills[:5]: # Show top 5
            try:
                row = QHBoxLayout()
                
                # Format: "Name - $10.00 (Due: Today)"
                symbol = bill.get('symbol')
                if not symbol:
                    # Robust lookup if symbol is missing in bill dict
                    symbol = "$" # Default
                    parent = self.parent()
                    if parent and hasattr(parent, 'currencies') and hasattr(parent, 'currencies_map'):
                        curr_code = bill.get('currency', '$ (USD)')
                        symbol = parent.currencies.get(parent.currencies_map.get(curr_code, '$ (USD)'), {}).get('symbol', '$')
                
                amount = bill.get('amount', 0.0)
                name = bill.get('name', 'Unnamed Bill')
                due_date = bill.get('due_date', 'No Date')
                
                text = f"<b>{name}</b><br>{symbol}{amount:,.2f} - {due_date}"
                lbl = QLabel(text)
                lbl.setStyleSheet("font-size: 10pt;")
                row.addWidget(lbl)
                
                pay_btn = QPushButton(STRINGS["btn_mark_paid"])
                pay_btn.setMinimumWidth(100)
                pay_btn.setStyleSheet(f"""
                    QPushButton {{
                        font-size: 9pt; 
                        padding: 6px; 
                        background-color: {p['success']}; 
                        color: white; 
                        border-radius: 4px; 
                        font-weight: bold;
                    }}
                    QPushButton:hover {{
                        background-color: #2a9d8f;
                    }}
                """)
                # Connect via lambda but need to handle closure
                pay_btn.clicked.connect(lambda checked, b=bill: self.mark_bill_paid(b))
                row.addWidget(pay_btn)
                container_layout.addLayout(row)
            except Exception as e:
                logging.error(f"Error rendering toast row: {e}")
                continue
        
        if len(self.bills) > 5:
            container_layout.addWidget(QLabel(f"<i>+ {len(self.bills)-5} more...</i>"))
            
        bills_scroll.setWidget(container)
        content_layout.addWidget(bills_scroll)
        
        # Global Footer
        footer = QHBoxLayout()
        open_btn = QPushButton(STRINGS["btn_view_details"])
        open_btn.setMinimumHeight(40)
        footer_contrast = self.theme_manager.get_contrast_color(accent)
        open_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {accent}; 
                color: {footer_contrast}; 
                font-weight: bold; 
                border-radius: 6px;
                font-size: 10pt;
            }}
            QPushButton:hover {{
                background-color: {accent};
                opacity: 0.9;
            }}
        """)
        open_btn.clicked.connect(self.open_app)
        footer.addWidget(open_btn)
        content_layout.addLayout(footer)
        
        main_layout.addWidget(self.main_frame)
        
        # Position at top right
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - self.width() - 20, 40)
        
        # Audio notification (Windows only)
        if platform.system() == 'Windows':
            try:
                winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)
            except: pass
            
        # Auto-close after 15 seconds
        QTimer.singleShot(15000, self.close)

    def mark_bill_paid(self, bill):
        parent = self.parent()
        if parent and hasattr(parent, 'pay_bill'):
            parent.pay_bill(bill)
        self.close()
        
    def open_app(self):
        parent = self.parent()
        if parent and hasattr(parent, 'show_window'):
            parent.show_window()
        self.close()

class PinEntryDialog(QDialog):
    """Dialog for entering the PIN to unlock the application."""
    def __init__(self, parent=None, mode='verify', can_minimize=False, hint=None):
        super().__init__(parent)
        self.mode = mode # 'verify', 'set'
        self.can_minimize = can_minimize
        self.hint = hint
        
        self.setWindowTitle(STRINGS["msg_app_locked"] if mode == 'verify' else STRINGS["group_security_pin"])
        self.setFixedSize(350, 450) if mode == 'set' else self.setFixedSize(350, 300)
        
        # Get theme manager from parent or singleton
        theme_manager = None
        if parent and hasattr(parent, 'theme_manager'):
            theme_manager = parent.theme_manager
        elif parent and parent.parent() and hasattr(parent.parent(), 'theme_manager'):
            theme_manager = parent.parent().theme_manager
        else:
            # Global fallback or finding it from main window
            for widget in QApplication.topLevelWidgets():
                if isinstance(widget, QMainWindow) and hasattr(widget, 'theme_manager'):
                    theme_manager = widget.theme_manager
                    break
        
        if not theme_manager:
            from Billtracker_qt import ThemeManager
            theme_manager = ThemeManager()
            
        p = theme_manager.get_palette()
        self.setStyleSheet(f"background-color: {p['bg']}; color: {p['text']};")
        
        layout = QVBoxLayout()
        label_text = STRINGS["label_pin_unlock"] if mode == 'verify' else STRINGS["label_pin_set_new"]
        self.label = QLabel(label_text)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 11pt; font-weight: bold;")
        layout.addWidget(self.label)
        
        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pin_input.setMaxLength(6)
        self.pin_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin_input.setPlaceholderText("****")
        self.pin_input.setStyleSheet(f"font-size: 18pt; padding: 5px; border-radius: 5px; background: {p['surface']}; color: {p['text']}; border: 1px solid {p['border']};")
        layout.addWidget(self.pin_input)
        
        if mode == 'set':
            # Confirm PIN
            self.confirm_label = QLabel(STRINGS["label_confirm_pin"])
            self.confirm_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(self.confirm_label)
            
            self.confirm_pin_input = QLineEdit()
            self.confirm_pin_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.confirm_pin_input.setMaxLength(6)
            self.confirm_pin_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.confirm_pin_input.setPlaceholderText(STRINGS["placeholder_confirm_pin"])
            self.confirm_pin_input.setStyleSheet(f"font-size: 18pt; padding: 5px; border-radius: 5px; background: {p['surface']}; color: {p['text']}; border: 1px solid {p['border']};")
            layout.addWidget(self.confirm_pin_input)
            
            # PIN Hint
            self.hint_setup_label = QLabel(STRINGS["label_pin_hint_setup"])
            self.hint_setup_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(self.hint_setup_label)
            
            self.hint_input = QLineEdit()
            self.hint_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.hint_input.setPlaceholderText(STRINGS["placeholder_hint"])
            self.hint_input.setStyleSheet(f"padding: 8px; border-radius: 5px; background: {p['surface']}; color: {p['text']}; border: 1px solid {p['border']};")
            layout.addWidget(self.hint_input)
            
        elif mode == 'verify' and self.hint:
            self.hint_display = QLabel(STRINGS["msg_pin_hint_prefix"].format(self.hint))
            self.hint_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.hint_display.setStyleSheet("font-style: italic; color: gray;")
            layout.addWidget(self.hint_display)

        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton(STRINGS["btn_unlock"] if mode == 'verify' else STRINGS["btn_save_pin"])
        self.ok_btn.clicked.connect(self.handle_accept)
        self.ok_btn.setDefault(True)
        accent = theme_manager.accent_color
        contrast = theme_manager.get_contrast_color(accent)
        self.ok_btn.setStyleSheet(f"background-color: {accent}; color: {contrast}; padding: 8px; font-weight: bold; border-radius: 4px;")
        btn_layout.addWidget(self.ok_btn)
        
        if mode != 'verify':
            self.cancel_btn = QPushButton(STRINGS["btn_cancel"])
            self.cancel_btn.clicked.connect(self.reject)
            self.cancel_btn.setStyleSheet(f"background-color: {p['surface']}; color: {p['text']}; padding: 8px; border-radius: 4px; border: 1px solid {p['border']};")
            btn_layout.addWidget(self.cancel_btn)
        
            
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def handle_accept(self):
        """Custom accept logic to handle PIN matching."""
        if self.mode == 'set':
            pin = self.pin_input.text().strip()
            confirm = self.confirm_pin_input.text().strip()
            
            if len(pin) < 4:
                QMessageBox.warning(self, STRINGS["title_invalid_pin"], STRINGS["msg_pin_too_short"])
                return
                
            if pin != confirm:
                QMessageBox.warning(self, STRINGS["title_invalid_pin"], STRINGS["msg_pins_dont_match"])
                return
        
        self.accept()

    def get_pin_hash(self):
        pin = self.pin_input.text().strip()
        if not pin or len(pin) < 4: return None
        return hashlib.sha256(pin.encode()).hexdigest()

    def get_pin_hint(self):
        if self.mode == 'set' and hasattr(self, 'hint_input'):
            return self.hint_input.text().strip()
        return ""


    def closeEvent(self, event):
        if self.mode == 'verify' and self.can_minimize:
            # Ask user: Minimize or Exit?
            msg = QMessageBox(self)
            msg.setWindowTitle(STRINGS["title_exit_min"])
            msg.setText(STRINGS["msg_exit_min"])
            btn_min = msg.addButton(STRINGS["btn_minimize"], QMessageBox.ButtonRole.ActionRole)
            btn_exit = msg.addButton(STRINGS["btn_exit"], QMessageBox.ButtonRole.DestructiveRole)
            btn_cancel = msg.addButton(STRINGS["btn_cancel"], QMessageBox.ButtonRole.RejectRole)
            msg.exec()
            
            if msg.clickedButton() == btn_exit:
                QApplication.quit()
            elif msg.clickedButton() == btn_min:
                self.done(102) # Custom code for Minimize
            else:
                event.ignore()
        else:
            super().closeEvent(event)

    def get_pin_hash(self):
        pin = self.pin_input.text().strip()
        if not pin or len(pin) < 4: return None
        return hashlib.sha256(pin.encode()).hexdigest()


class CurrencySelectorDialog(QDialog):
    """Searchable currency selector dialog."""
    def __init__(self, parent, currencies, current_currency=None):
        super().__init__(parent)
        self.setWindowTitle(STRINGS["title_select_currency"])
        self.setGeometry(100, 100, 400, 500)
        self.currencies = currencies
        self.selected_currency = current_currency
        
        layout = QVBoxLayout()
        
        # Search input
        search_label = QLabel(STRINGS["label_search_currency"])
        layout.addWidget(search_label)
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.filter_currencies)
        layout.addWidget(self.search_input)
        
        # Currency list
        self.currency_list = QListWidget()
        self.currency_list.itemDoubleClicked.connect(self.select_currency)
        layout.addWidget(self.currency_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton(STRINGS["btn_ok"])
        ok_button.clicked.connect(self.on_ok)
        cancel_button = QPushButton(STRINGS["btn_cancel"])
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.populate_list()
        self.search_input.setFocus()
    
    def populate_list(self, filter_text=""):
        self.currency_list.clear()
        filter_lower = filter_text.lower()
        
        for display_key, meta in self.currencies.items():
            code = meta['code']
            symbol = meta['symbol']
            
            # Search in the display key, code, and symbol
            if (filter_lower == "" or 
                filter_lower in display_key.lower() or 
                filter_lower in code.lower() or 
                filter_lower in symbol.lower()):
                item = QListWidgetItem(display_key)
                item.setData(Qt.ItemDataRole.UserRole, display_key)
                self.currency_list.addItem(item)
    
    def filter_currencies(self):
        self.populate_list(self.search_input.text())
    
    def select_currency(self, item):
        self.selected_currency = item.data(Qt.ItemDataRole.UserRole)
        self.accept()
    
    def on_ok(self):
        current_item = self.currency_list.currentItem()
        if current_item:
            self.selected_currency = current_item.data(Qt.ItemDataRole.UserRole)
            self.accept()
        else:
            # No item selected, just close dialog without changing the selection
            self.reject()
    
    def get_selected_currency(self):
        return self.selected_currency


def get_cached_icon(path):
    """Return cached QIcon/QPixmap for path; simple cache to avoid repeated disk loads."""
    from PyQt6.QtGui import QIcon, QPixmap
    if not hasattr(get_cached_icon, '_cache'):
        get_cached_icon._cache = {}
    cache = get_cached_icon._cache
    if path in cache:
        return cache[path]
    try:
        pix = QPixmap(path)
        icon = QIcon(pix)
        cache[path] = icon
        return icon
    except Exception:
        return None


class BillEditorDialog(QDialog):
    """Dialog for editing a bill."""
    def __init__(self, parent, bill, currencies):
        super().__init__(parent)
        self.bill = bill
        self.currencies = currencies
        self.setWindowTitle(STRINGS["edit_bill_title"])
        self.setGeometry(100, 100, 450, 350)
        
        layout = QFormLayout()
        
        self.name_input = QLineEdit(bill['name'])
        layout.addRow(STRINGS["bill_name_label"] + ":", self.name_input)
        
        self.amount_input = QLineEdit(str(bill['amount']))
        layout.addRow(STRINGS["amount_label"] + ":", self.amount_input)
        
        # Currency with search button
        currency_layout = QHBoxLayout()
        self.currency_combo = QComboBox()
        
        # Standardize to Popular + used currencies (v6.7.2)
        if hasattr(parent, 'get_filtered_currency_list'):
            items = parent.get_filtered_currency_list()
        else:
            items = list(currencies.keys())
        
        self.currency_combo.addItems(items)
        
        # Ensure current bill currency is present if not in filtered list
        if bill['currency'] and self.currency_combo.findText(bill['currency']) == -1:
            self.currency_combo.addItem(bill['currency'])
            
        self.currency_combo.setCurrentText(bill['currency'])
        currency_layout.addWidget(self.currency_combo)
        
        search_currency_btn = QPushButton(STRINGS["btn_search"])
        search_currency_btn.clicked.connect(self.open_currency_selector)
        currency_layout.addWidget(search_currency_btn)
        layout.addRow(STRINGS["currency_label"] + ":", currency_layout)
        

        
        self.category_combo = QComboBox()
        self.category_combo.addItems(CATEGORIES)
        self.category_combo.setCurrentText(get_display_category(bill.get('category', 'Other')))
        layout.addRow(STRINGS["category_label"] + ":", self.category_combo)
        
        self.repeat_combo = QComboBox()
        self.repeat_combo.addItems(FREQUENCIES)
        self.repeat_combo.setCurrentText(get_display_frequency(bill.get('repeat_freq', 'No Repeat')))
        layout.addRow(STRINGS["repeat_label"] + ":", self.repeat_combo)
        
        self.date_input = QDateEdit()
        try:
            due_date = datetime.strptime(bill['due_date'], '%Y-%m-%d').date()
            self.date_input.setDate(QDate(due_date.year, due_date.month, due_date.day))
        except:
            self.date_input.setDate(QDate.currentDate())
        layout.addRow(STRINGS["due_date_label"] + ":", self.date_input)
        
        self.is_subscription_chk = QCheckBox(STRINGS["chk_is_subscription"])
        self.is_subscription_chk.setChecked(bill.get('is_subscription', False))
        layout.addRow("", self.is_subscription_chk)
        
        save_button = QPushButton(STRINGS["save_changes_button"])
        save_button.clicked.connect(self.accept)
        layout.addRow(save_button)
        
        self.setLayout(layout)
    
    def open_currency_selector(self):
        """Open searchable currency selector for BillEditor."""
        dialog = CurrencySelectorDialog(self, self.currencies, self.currency_combo.currentText())
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected = dialog.get_selected_currency()
            if selected:
                # Ensure it's in the list (v6.7.4)
                if self.currency_combo.findText(selected) == -1:
                    self.currency_combo.addItem(selected)
                self.currency_combo.setCurrentText(selected)
    
    def get_data(self):
        try:
            amount = strict_float(self.amount_input.text()) # Hardened
            if amount <= 0:
                raise ValueError
            if amount > 1000000000: # 1 Billion limit
                QMessageBox.warning(self, STRINGS["dialog_input_error"], STRINGS["msg_amount_large"])
                return None
        except ValueError:
            QMessageBox.warning(self, STRINGS["dialog_input_error"], STRINGS["error_positive_amount"])
            return None
        
        return {
            'name': sanitize_input(self.name_input.text()), # Hardened
            'amount': amount,
            'currency': self.currency_combo.currentText(),
            'category': get_canonical_category(self.category_combo.currentText()),
            'repeat_freq': get_canonical_frequency(self.repeat_combo.currentText()),
            'due_date': self.date_input.date().toString('yyyy-MM-dd'),
            'is_subscription': self.is_subscription_chk.isChecked()
        }


class ConverterWindow(QDialog):
    """Currency converter dialog."""
    def __init__(self, parent, currencies, exchange_rates):
        super().__init__(parent)
        self.currencies = currencies
        self.exchange_rates = exchange_rates
        self.setWindowTitle(STRINGS["converter_title"])
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        
        # Amount input
        layout.addWidget(QLabel(STRINGS["amount_label"] + ":"))
        self.amount_input = QLineEdit("1.00")
        layout.addWidget(self.amount_input)
        
        # From currency
        layout.addWidget(QLabel(STRINGS["from_label"] + ":"))
        from_layout = QHBoxLayout()
        # Filtered list: popular + GEL
        provider = lambda: self.parent().get_filtered_currency_list()
        self.from_combo = LazyCombo(provider)
        
        # Select default: "$ - United States Dollar"
        for key, meta in currencies.items():
            if meta['code'] == 'USD':
                self.from_combo.pending_text = key
                break
                
        from_layout.addWidget(self.from_combo)
        
        from_search_btn = QPushButton("🔍")
        from_search_btn.setFixedWidth(40)
        from_search_btn.clicked.connect(lambda: self.open_currency_search(self.from_combo))
        from_layout.addWidget(from_search_btn)
        layout.addLayout(from_layout)
        
        # To currency
        layout.addWidget(QLabel(STRINGS["to_label"] + ":"))
        to_layout = QHBoxLayout()
        self.to_combo = LazyCombo(provider)
        
        # Select default: "₾ - Georgian Lari" or "€ - Euro"
        for key, meta in currencies.items():
            if meta['code'] == 'GEL':
                self.to_combo.pending_text = key
                break
            elif meta['code'] == 'EUR': # Secondary fallback
                self.to_combo.pending_text = key

        to_layout.addWidget(self.to_combo)
        
        to_search_btn = QPushButton("🔍")
        to_search_btn.setFixedWidth(40)
        to_search_btn.clicked.connect(lambda: self.open_currency_search(self.to_combo))
        to_layout.addWidget(to_search_btn)
        layout.addLayout(to_layout)
        
        # Result
        self.result_label = QLabel("0.00")
        result_font = QFont()
        result_font.setPointSize(14)
        result_font.setBold(True)
        self.result_label.setFont(result_font)
        layout.addWidget(self.result_label)
        
        # Convert button
        convert_btn = QPushButton(STRINGS["convert_button"])
        convert_btn.clicked.connect(self.convert)
        layout.addWidget(convert_btn)
        
        copy_button = QPushButton(STRINGS["btn_copy_result"])
        copy_button.clicked.connect(self.copy_result)
        layout.addWidget(copy_button)
        
        # 30-Day Trend
        layout.addSpacing(10)
        layout.addWidget(QLabel(STRINGS["lbl_trend_30d"] + ":"))
        self.sparkline = SparklineWidget()
        layout.addWidget(self.sparkline)
        
        self.setLayout(layout)
        
        # Initial history fetch
        QTimer.singleShot(500, self.fetch_history)
    
    def convert(self):
        try:
            amount = strict_float(self.amount_input.text()) # Hardened
            from_curr = self.from_combo.currentText()
            to_curr = self.to_combo.currentText()
            
            from_rate = self.exchange_rates.get(from_curr, 1.0)
            to_rate = self.exchange_rates.get(to_curr, 1.0)
            
            if from_rate > 0:
                result = (amount / from_rate) * to_rate
                meta = self.currencies.get(to_curr, {'symbol': '$'})
                symbol = meta.get('symbol', '$')
                self.result_label.setText(f"{symbol}{result:,.2f}")
            else:
                self.result_label.setText(STRINGS["title_error"])
        except ValueError:
            self.result_label.setText(STRINGS["invalid_input"])
        
        # Update history trend when converting
        self.fetch_history()

    def fetch_history(self):
        """Fetch 30-day history for the selected currency pair."""
        from_text = self.from_combo.currentText()
        to_text = self.to_combo.currentText()
        
        from_meta = self.currencies.get(from_text)
        to_meta = self.currencies.get(to_text)
        
        if from_meta and to_meta:
            f_code = from_meta['code']
            t_code = to_meta['code']
            
            self.history_thread = HistoryAPIThread(f_code, t_code)
            self.history_thread.finished.connect(self.sparkline.set_data)
            self.history_thread.start()

    def copy_result(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.result_label.text())
        QMessageBox.information(self, STRINGS["title_copied"], STRINGS["msg_copied"])

    def open_currency_search(self, combo_box):
        """Open searchable currency selector for a combo box."""
        dialog = CurrencySelectorDialog(self, self.currencies, combo_box.currentText())
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected = dialog.get_selected_currency()
            if selected:
                # Ensure it's in the list (v6.7.4)
                if combo_box.findText(selected) == -1:
                    combo_box.addItem(selected)
                combo_box.setCurrentText(selected)


class SavingsGoalDialog(QDialog):
    """Dialog to create or edit a savings goal."""
    def __init__(self, parent, goal=None):
        super().__init__(parent)
        self.goal = goal or {'name': '', 'target': 100.0, 'current': 0.0, 'currency': 'USD'}
        self.currencies = parent.currencies
        self.setWindowTitle(STRINGS["btn_add_goal"])
        self.setGeometry(100, 100, 400, 300)
        
        layout = QFormLayout()
        
        self.name_input = QLineEdit(self.goal['name'])
        layout.addRow(STRINGS["lbl_goal_name"] + ":", self.name_input)
        
        self.target_input = QDoubleSpinBox()
        self.target_input.setRange(1.0, 1000000000.0)
        self.target_input.setValue(float(self.goal['target']))
        self.target_input.setPrefix("$ ")
        layout.addRow(STRINGS["lbl_target_amount"] + ":", self.target_input)
        
        self.current_input = QDoubleSpinBox()
        self.current_input.setRange(0.0, 1000000000.0)
        self.current_input.setValue(float(self.goal['current']))
        layout.addRow(STRINGS["lbl_current_amount"] + ":", self.current_input)
        
        # Currency Row with Search
        currency_row = QHBoxLayout()
        self.currency_combo = QComboBox()
        
        # Standardize to Popular + used currencies (v6.7.2)
        if hasattr(parent, 'get_filtered_currency_list'):
            items = parent.get_filtered_currency_list()
        elif hasattr(parent, 'main_window') and hasattr(parent.main_window, 'get_filtered_currency_list'):
            items = parent.main_window.get_filtered_currency_list()
        else:
            items = list(self.currencies.keys())
            
        self.currency_combo.addItems(items)
        
        # Ensure current goal currency is present
        g_curr = self.goal.get('currency', 'USD')
        if g_curr and self.currency_combo.findText(g_curr) == -1:
            self.currency_combo.addItem(g_curr)
            
        self.currency_combo.setCurrentText(g_curr)
        currency_row.addWidget(self.currency_combo)
        
        search_btn = QPushButton("🔍")
        search_btn.setFixedWidth(40)
        search_btn.clicked.connect(self.open_currency_search)
        currency_row.addWidget(search_btn)
        
        layout.addRow(STRINGS["currency_label"] + ":", currency_row)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
        self.setLayout(layout)

    def open_currency_search(self):
        """Open searchable currency selector for SavingsGoalDialog."""
        dialog = CurrencySelectorDialog(self, self.currencies, self.currency_combo.currentText())
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected = dialog.get_selected_currency()
            if selected:
                # Ensure it's in the list (v6.7.4)
                if self.currency_combo.findText(selected) == -1:
                    self.currency_combo.addItem(selected)
                combo_box.setCurrentText(selected)

    def get_data(self):
        return {
            'name': sanitize_input(self.name_input.text()),
            'target': self.target_input.value(),
            'current': self.current_input.value(),
            'currency': self.currency_combo.currentText()
        }

class SavingsTab(QWidget):
    """Tab for managing savings goals and tracking progress."""
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Summary Area
        summary_group = QGroupBox(STRINGS["tab_savings"])
        summary_layout = QGridLayout()
        
        self.total_saved_label = QLabel(f"{STRINGS['lbl_total_saved']} $0.00")
        p = self.main_window.theme_manager.get_palette()
        self.total_saved_label.setStyleSheet(f"font-size: 14pt; font-weight: bold; color: {p['success']};")
        summary_layout.addWidget(self.total_saved_label, 0, 0, 1, 2)
        
        add_goal_btn = QPushButton(STRINGS["btn_add_goal"])
        add_goal_btn.clicked.connect(self.add_goal)
        summary_layout.addWidget(add_goal_btn, 1, 0)
        
        summary_group.setLayout(summary_layout)
        layout.addWidget(summary_group)
        
        # Goals List
        self.goals_scroll = QScrollArea()
        self.goals_scroll.setWidgetResizable(True)
        self.goals_content = QWidget()
        self.goals_layout = QVBoxLayout(self.goals_content)
        self.goals_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.goals_scroll.setWidget(self.goals_content)
        layout.addWidget(self.goals_scroll)
        
        self.setLayout(layout)

    def add_goal(self):
        dialog = SavingsGoalDialog(self.main_window)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.main_window.savings_goals.append(dialog.get_data())
            self.main_window.save_data()
            self.refresh_data()

    def edit_goal(self, goal_index):
        goal = self.main_window.savings_goals[goal_index]
        dialog = SavingsGoalDialog(self.main_window, goal)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.main_window.savings_goals[goal_index] = dialog.get_data()
            self.main_window.save_data()
            self.refresh_data()

    def delete_goal(self, goal_index):
        reply = QMessageBox.question(self, STRINGS["dialog_confirm_delete"], 
                                   STRINGS["confirm_delete_msg"].format(self.main_window.savings_goals[goal_index]['name']))
        if reply == QMessageBox.StandardButton.Yes:
            self.main_window.savings_goals.pop(goal_index)
            self.main_window.save_data()
            self.refresh_data()

    def add_savings_funds(self, goal_index):
        """Quickly add funds to a savings goal."""
        goal = self.main_window.savings_goals[goal_index]
        amount, ok = QInputDialog.getDouble(self, STRINGS["btn_add"], 
                                         f"{goal['name']} ({goal['currency']}):", 
                                         0, 0, 1000000, 2)
        if ok and amount > 0:
            goal['current'] = float(goal['current']) + amount
            self.main_window.save_data()
            self.refresh_data()
            self.main_window.update_display() # Update dashboard too

    def refresh_data(self):
        # Clear existing entries
        for i in reversed(range(self.goals_layout.count())): 
            widget = self.goals_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
            
        total_saved_usd = 0.0
        
        for i, goal in enumerate(self.main_window.savings_goals):
            p = self.main_window.theme_manager.get_palette()
            goal_card = QFrame()
            goal_card.setFrameShape(QFrame.Shape.StyledPanel)
            # Use success color for the subtle background pulse effect
            goal_card.setStyleSheet(f"QFrame {{ background-color: {p['success']}11; border-radius: 10px; padding: 10px; margin-bottom: 5px; border: 1px solid {self.main_window.accent_color}44; }}")
            
            card_layout = QVBoxLayout(goal_card)
            
            header = QHBoxLayout()
            name_lbl = QLabel(f"<b>{goal['name']}</b>")
            header.addWidget(name_lbl)
            
            edit_btn = QPushButton("✏️")
            edit_btn.setFixedWidth(35) # Slightly wider for emoji
            edit_btn.setStyleSheet("padding: 2px;") # Reset excessive global padding
            edit_btn.clicked.connect(lambda chk, idx=i: self.edit_goal(idx))
            header.addWidget(edit_btn)
            
            add_funds_btn = QPushButton("➕")
            add_funds_btn.setFixedWidth(35)
            # Use accent color for add button
            a_contrast = self.main_window.theme_manager.get_contrast_color(self.main_window.accent_color)
            add_funds_btn.setStyleSheet(f"padding: 2px; background-color: {self.main_window.accent_color}; color: {a_contrast};")
            add_funds_btn.clicked.connect(lambda chk, idx=i: self.add_savings_funds(idx))
            header.addWidget(add_funds_btn)
            
            del_btn = QPushButton("🗑️")
            del_btn.setFixedWidth(35)
            d_contrast = self.main_window.theme_manager.get_contrast_color(p['danger'])
            del_btn.setStyleSheet(f"padding: 2px; background-color: {p['danger']}; color: {d_contrast};") # Reset padding + distinct color
            del_btn.clicked.connect(lambda chk, idx=i: self.delete_goal(idx))
            header.addWidget(del_btn)
            
            card_layout.addLayout(header)
            
            # Progress calculation
            cur = float(goal['current'])
            target = float(goal['target'])
            percent = min(100, int((cur / target) * 100)) if target > 0 else 0
            
            progress = QProgressBar()
            progress.setValue(percent)
            p_contrast = self.main_window.theme_manager.get_contrast_color(p['success'])
            progress.setStyleSheet(f"QProgressBar {{ height: 15px; border: none; background-color: {p['surface']}; border: 1px solid {p['border']}; border-radius: 7px; text-align: center; color: {p['text']}; }} QProgressBar::chunk {{ background-color: {p['success']}; border-radius: 7px; }}")
            card_layout.addWidget(progress)
            
            # Extract symbol correctly (fix v6.7.3)
            metadata = self.main_window.currencies.get(goal['currency'], {'symbol': '$'})
            symbol = metadata.get('symbol', '$') if isinstance(metadata, dict) else metadata
            
            stats = QLabel(f"{symbol}{cur:,.2f} / {symbol}{target:,.2f} ({percent}%)")
            stats.setAlignment(Qt.AlignmentFlag.AlignRight)
            card_layout.addWidget(stats)
            
            self.goals_layout.addWidget(goal_card)
            
            # Convert to USD for total summary (Ensure robust rate lookup)
            rate = self.main_window.get_exchange_rate(goal['currency'])
            
            if rate > 0:
                total_saved_usd += cur / (rate or 1.0)

        self.total_saved_label.setText(f"Total Saved: ${total_saved_usd:,.2f} (USD)")


class BillDetailsDialog(QDialog):
    """Dialog to show bill details and actions."""
    def __init__(self, parent, bill, currencies, is_paid=False):
        super().__init__(parent)
        self.setWindowTitle(STRINGS["menu_view_details"])
        self.setGeometry(100, 100, 400, 350)
        
        layout = QVBoxLayout()
        
        # Details Form
        form = QFormLayout()
        
        # Name
        name_label = QLabel(bill['name'])
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        name_label.setFont(font)
        form.addRow(STRINGS["header_name"] + ":", name_label)
        
        # Amount
        metadata = currencies.get(bill['currency'], {'symbol': '$'})
        symbol = metadata.get('symbol', '$') if isinstance(metadata, dict) else metadata
        amount_label = QLabel(f"{symbol}{bill['amount']:,.2f}")
        amount_label.setFont(font)
        form.addRow(STRINGS["header_amount"] + ":", amount_label)
        
        # Category
        cat_display = get_display_category(bill.get('category', 'Other'))
        form.addRow(STRINGS["header_category"] + ":", QLabel(cat_display))
        
        # Date
        date_label = STRINGS["header_paid_date"] if is_paid else STRINGS["header_due_date"]
        form.addRow(date_label + ":", QLabel(bill.get('due_date', '-')))
        
        # Frequency
        freq_display = get_display_frequency(bill.get('repeat_freq', 'No Repeat'))
        form.addRow(STRINGS["header_frequency"] + ":", QLabel(freq_display))
        
        # Status
        status_text = STRINGS["status_paid"] if is_paid else STRINGS["status_unpaid"]
        status_label = QLabel(status_text)
        if not is_paid:
            status_label.setStyleSheet("color: #e63946; font-weight: bold;")
        else:
            status_label.setStyleSheet("color: #2a9d8f; font-weight: bold;")
        form.addRow(STRINGS["header_status"] + ":", status_label)
        
        layout.addLayout(form)
        
        layout.addSpacing(20)
        
        # Actions
        self.action_code = 0
        btn_layout = QHBoxLayout()
        
        if not is_paid:
            pay_btn = QPushButton(STRINGS["menu_pay_bill"])
            pay_btn.clicked.connect(lambda: self.done_action(1)) # 1 = Pay
            btn_layout.addWidget(pay_btn)
            
            edit_btn = QPushButton(STRINGS["menu_edit_bill"])
            edit_btn.clicked.connect(lambda: self.done_action(2)) # 2 = Edit
            btn_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton(STRINGS["menu_delete_bill"])
        delete_btn.setStyleSheet("background-color: #e63946; color: white;")
        delete_btn.clicked.connect(lambda: self.done_action(3)) # 3 = Delete
        btn_layout.addWidget(delete_btn)
        
        layout.addLayout(btn_layout)
        
        close_btn = QPushButton(STRINGS["btn_cancel"])
        close_btn.clicked.connect(self.reject)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)

    def done_action(self, code):
        self.action_code = code
        self.accept()
    
    def browse_sync_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Sync Folder")
        if folder:
            self.sync_path_input.setText(folder)

    def get_action(self):
        return self.action_code


class CategoryManagerDialog(QDialog):
    """Dialog to add or remove custom categories."""
    def __init__(self, parent, custom_categories):
        super().__init__(parent)
        self.setWindowTitle(STRINGS["title_manage_categories"])
        self.setFixedSize(300, 400)
        self.custom_categories = custom_categories
        self.deleted_categories = []
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel(STRINGS["label_manage_categories_hint"]))
        
        self.list_widget = QListWidget()
        self.list_widget.addItems(self.custom_categories)
        layout.addWidget(self.list_widget)
        
        self.new_cat_input = QLineEdit()
        self.new_cat_input.setPlaceholderText(STRINGS["placeholder_new_category"])
        layout.addWidget(self.new_cat_input)
        
        btn_layout = QHBoxLayout()
        add_btn = QPushButton(STRINGS["btn_add"])
        add_btn.clicked.connect(self.add_category)
        btn_layout.addWidget(add_btn)
        
        del_btn = QPushButton(STRINGS["btn_remove"])
        del_btn.clicked.connect(self.remove_selected)
        btn_layout.addWidget(del_btn)
        layout.addLayout(btn_layout)
        
        # Bottom Buttons
        bottom_btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        bottom_btns.accepted.connect(self.accept)
        bottom_btns.rejected.connect(self.reject)
        layout.addWidget(bottom_btns)
        
        self.setLayout(layout)

    def add_category(self):
        text = self.new_cat_input.text().strip()
        if text and text not in self.custom_categories and text not in CANONICAL_CATEGORIES:
            self.custom_categories.append(text)
            self.list_widget.addItem(text)
            self.new_cat_input.clear()

    def remove_selected(self):
        item = self.list_widget.currentItem()
        if item:
            cat = item.text()
            self.custom_categories.remove(cat)
            self.deleted_categories.append(cat)
            self.list_widget.takeItem(self.list_widget.row(item))

    def get_data(self):
        return self.custom_categories

def get_full_categories(custom_list):
    """Return merged list of default and custom categories."""
    return STRINGS['categories_list'] + custom_list


class MiniTrackerWidget(QWidget):
    """A compact, always-on-top widget for quick budget/due bills check."""
    def __init__(self, parent=None, strings=None, theme_manager=None):
        super().__init__(None) # No parent to allow separate window
        self.main_window = parent
        self.STRINGS = strings
        self.theme_manager = theme_manager
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.init_ui()
        self.update_data()
        
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.container = QFrame()
        self.container.setObjectName("MiniContainer")
        
        # Style based on theme
        p = self.theme_manager.get_palette()
        accent = self.theme_manager.accent_color
        bg = p['bg']
        text_color = p['text']
        btn_contrast = self.theme_manager.get_contrast_color(accent)
        
        self.container.setStyleSheet(f"""
            QFrame#MiniContainer {{
                background-color: {bg};
                border: 2px solid {accent};
                border-radius: 15px;
            }}
            QLabel {{
                color: {text_color};
                background: transparent;
                font-family: 'Segoe UI', sans-serif;
            }}
            QPushButton {{
                background-color: {accent};
                color: {btn_contrast};
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                opacity: 0.9;
            }}
        """)
        
        container_layout = QVBoxLayout(self.container)
        
        # Title/Drag Handle
        title = QLabel(self.STRINGS["title_mini_mode"])
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Determine if accent is readable against background
        bg_contrast = self.theme_manager.get_contrast_color(bg)
        acc_contrast = self.theme_manager.get_contrast_color(accent)
        
        display_accent = accent
        if bg_contrast == acc_contrast:
            # Accent is on the same "side" of luminance as background (e.g. Yellow on White)
            # Use the contrasting color of the background for the title to be safe
            display_accent = bg_contrast
            
        title.setStyleSheet(f"font-weight: bold; font-size: 10pt; color: {display_accent}; background: transparent;")
        container_layout.addWidget(title)
        
        # Budget info
        self.budget_lbl = QLabel(self.STRINGS["lbl_budget_rem"] + " --")
        self.budget_lbl.setStyleSheet("font-size: 11pt; background: transparent;")
        self.budget_lbl.setWordWrap(True)
        container_layout.addWidget(self.budget_lbl)
        
        # Due today info
        self.due_lbl = QLabel(f"{STRINGS['lbl_due_today']} 0")
        self.due_lbl.setWordWrap(True)
        self.due_lbl.setStyleSheet("background: transparent;")
        container_layout.addWidget(self.due_lbl)
        
        # Buttons
        btn_row = QHBoxLayout()
        
        self.btn_refresh = QPushButton("↻")
        self.btn_refresh.setFixedWidth(30)
        self.btn_refresh.clicked.connect(self.update_data)
        btn_row.addWidget(self.btn_refresh)
        
        self.btn_restore = QPushButton(self.STRINGS["btn_full_mode"])
        self.btn_restore.clicked.connect(self.restore_main)
        btn_row.addWidget(self.btn_restore)
        
        container_layout.addLayout(btn_row)
        
        self.layout.addWidget(self.container)
        self.setLayout(self.layout)
        
        # Drop shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 0)
        self.container.setGraphicsEffect(shadow)
        
        self.setFixedSize(250, 170)
        
        # Position at bottom right
        screen = QApplication.primaryScreen().availableGeometry()
        self.move(screen.width() - 270, screen.height() - 190)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_pos)
            event.accept()

    def update_data(self):
        if not self.main_window: return
        
        # Get budget remaining
        remaining = self.main_window.get_budget_remaining() # We'll need to expose this
        self.budget_lbl.setText(f"{self.STRINGS['lbl_budget_rem']} {remaining}")
        
        # Get bills due today
        today = date.today().strftime('%Y-%m-%d')
        due_today_count = sum(1 for b in self.main_window.unpaid_bills if b['due_date'] == today)
        self.due_lbl.setText(f"{STRINGS['lbl_due_today']} {due_today_count}")

    def restore_main(self):
        if self.main_window:
            self.main_window.show()
            self.main_window.raise_()
            self.main_window.activateWindow()
        self.close()

class CSVImportDialog(QDialog):
    """Dialog for importing bills from a CSV bank statement."""
    def __init__(self, parent, currencies):
        super().__init__(parent)
        self.currencies = currencies
        self.setWindowTitle(STRINGS["title_csv_import"])
        self.setMinimumWidth(600)
        
        self.csv_data = []
        self.headers = []
        
        layout = QVBoxLayout()
        
        # File Selection
        file_layout = QHBoxLayout()
        self.file_label = QLabel(STRINGS["lbl_no_file_selected"])
        file_layout.addWidget(self.file_label)
        
        select_btn = QPushButton(STRINGS["btn_select_csv"])
        select_btn.clicked.connect(self.select_file)
        file_layout.addWidget(select_btn)
        layout.addLayout(file_layout)
        
        # Mapping Group
        self.mapping_group = QGroupBox(STRINGS["group_column_mapping"])
        mapping_layout = QGridLayout()
        
        self.name_map = QComboBox()
        self.amount_map = QComboBox()
        self.date_map = QComboBox()
        
        mapping_layout.addWidget(QLabel(STRINGS["lbl_map_name"] + ":"), 0, 0)
        mapping_layout.addWidget(self.name_map, 0, 1)
        mapping_layout.addWidget(QLabel(STRINGS["lbl_map_amount"] + ":"), 1, 0)
        mapping_layout.addWidget(self.amount_map, 1, 1)
        mapping_layout.addWidget(QLabel(STRINGS["lbl_map_date"] + ":"), 2, 0)
        mapping_layout.addWidget(self.date_map, 2, 1)
        
        self.mapping_group.setLayout(mapping_layout)
        self.mapping_group.setEnabled(False)
        layout.addWidget(self.mapping_group)
        
        # Preview Table
        layout.addWidget(QLabel(STRINGS["lbl_preview_top_5"]))
        self.preview_table = QTableWidget(5, 3)
        self.preview_table.setHorizontalHeaderLabels(["Name", "Amount", "Date"])
        self.preview_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.preview_table)
        
        # Buttons
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(self.process_import)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)
        
        self.setLayout(layout)

    def select_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if path:
            self.file_label.setText(os.path.basename(path))
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    self.csv_data = list(reader)
                    if self.csv_data:
                        self.headers = self.csv_data[0]
                        self.name_map.clear()
                        self.amount_map.clear()
                        self.date_map.clear()
                        self.name_map.addItems(self.headers)
                        self.amount_map.addItems(self.headers)
                        self.date_map.addItems(self.headers)
                        
                        # Try to guess mapping
                        for i, h in enumerate(self.headers):
                            h_low = h.lower()
                            if any(x in h_low for x in ['name', 'desc', 'payee', 'merchant']):
                                self.name_map.setCurrentIndex(i)
                            if any(x in h_low for x in ['amount', 'price', 'total', 'value']):
                                self.amount_map.setCurrentIndex(i)
                            if any(x in h_low for x in ['date', 'time', 'period']):
                                self.date_map.setCurrentIndex(i)
                        
                        self.mapping_group.setEnabled(True)
                        self.update_preview()
            except Exception as e:
                QMessageBox.critical(self, STRINGS["title_error"], STRINGS["msg_csv_read_failed"].format(e))

    def update_preview(self):
        self.preview_table.setRowCount(0)
        if len(self.csv_data) <= 1: return
        
        rows = self.csv_data[1:6]
        self.preview_table.setRowCount(len(rows))
        
        ni = self.name_map.currentIndex()
        ai = self.amount_map.currentIndex()
        di = self.date_map.currentIndex()
        
        for r, row in enumerate(rows):
            try:
                self.preview_table.setItem(r, 0, QTableWidgetItem(row[ni] if ni < len(row) else ""))
                self.preview_table.setItem(r, 1, QTableWidgetItem(row[ai] if ai < len(row) else ""))
                self.preview_table.setItem(r, 2, QTableWidgetItem(row[di] if di < len(row) else ""))
            except: pass

    def process_import(self):
        if not self.csv_data or len(self.csv_data) <= 1:
            self.reject()
            return
            
        ni = self.name_map.currentIndex()
        ai = self.amount_map.currentIndex()
        di = self.date_map.currentIndex()
        
        self.imported_bills = []
        
        # Keyword map for auto-categorization
        cat_map = {
            'uber': 'Transport', 'bolt': 'Transport', 'taxi': 'Transport',
            'netflix': 'Subscriptions', 'spotify': 'Subscriptions', 'apple.com': 'Subscriptions',
            'gym': 'Personal', 'pharmacy': 'Health', 'clinic': 'Health',
            'amazon': 'Other', 'ebay': 'Other',
            'market': 'Food', 'store': 'Food', 'restaurant': 'Food', 'cafe': 'Food',
            'electric': 'Utilities', 'water': 'Utilities', 'gas': 'Utilities', 'internet': 'Utilities'
        }
        
        for row in self.csv_data[1:]:
            try:
                if len(row) <= max(ni, ai, di): continue
                
                name = row[ni].strip()
                amount_str = row[ai].strip()
                # Use strict_float for safety (v6.3.1 hardening)
                amount = abs(strict_float(amount_str))
                raw_date = row[di].strip()
                
                # Try to parse date or default to today
                try:
                    # Generic parser attempts
                    for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%b %d, %Y'):
                        try:
                            dt = datetime.strptime(raw_date, fmt)
                            raw_date = dt.strftime('%Y-%m-%d')
                            break
                        except: continue
                except:
                    raw_date = date.today().strftime('%Y-%m-%d')
                
                # Auto-categorize
                category = 'Other'
                name_low = name.lower()
                for key, val in cat_map.items():
                    if key in name_low:
                        category = val
                        break
                
                # Use app's default currency if detection fails (v6.3.1)
                default_curr = "USD"
                if hasattr(self.parent(), 'bill_currency_combo'):
                    default_curr = self.parent().bill_currency_combo.currentText()
                
                bill = {
                    'name': name,
                    'amount': amount,
                    'currency': default_curr,
                    'due_date': raw_date,
                    'category': category,
                    'repeat_freq': 'No Repeat',
                    'notes': f'Imported (v6.3.1)'
                }
                self.imported_bills.append(bill)
            except Exception as e:
                logging.debug(f"CSV Row Import Skip: {e}")
                continue
            
        if self.imported_bills:
            self.accept()
        else:
            QMessageBox.warning(self, STRINGS["title_csv_import"], STRINGS["msg_csv_invalid"])

    def get_imported_bills(self):
        return self.imported_bills


class SettingsDialog(QDialog):
    """Settings dialog."""
    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.data_manager = data_manager
        self.theme_manager = parent.theme_manager if hasattr(parent, 'theme_manager') else None
        self.setWindowTitle(STRINGS["settings_title"])
        self.setMinimumWidth(550)
        
        layout = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        form_layout = QFormLayout(scroll_content)
        
        if hasattr(parent, 'session_pin'):
            self.session_pin = parent.session_pin
        else:
            self.session_pin = None
            
        config = self.data_manager.load_config(self.session_pin)

        # 1. Backups & Recovery (Moved to top as requested)
        backup_group_title = STRINGS["group_backups"].replace('&', '&&')
        backup_group = QGroupBox(backup_group_title)
        backup_layout = QVBoxLayout()
        
        # Location
        loc_row = QHBoxLayout()
        loc_row.addWidget(QLabel(STRINGS["lbl_backup_location"] + ":"))
        self.backup_path_input = QLineEdit()
        current_backup = config.get('backup_dir', '')
        if not current_backup:
            current_backup = os.path.join(self.data_manager.config_dir, 'backups')
        self.backup_path_input.setText(current_backup)
        self.backup_path_input.setReadOnly(True)
        loc_row.addWidget(self.backup_path_input)
        
        browse_backup_btn = QPushButton()
        browse_backup_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon))
        browse_backup_btn.setFixedWidth(30)
        browse_backup_btn.clicked.connect(self.browse_backup_location)
        loc_row.addWidget(browse_backup_btn)
        
        reset_backup_btn = QPushButton()
        reset_backup_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload))
        reset_backup_btn.setFixedWidth(30)
        reset_backup_btn.setToolTip(STRINGS["btn_reset_default"])
        reset_backup_btn.clicked.connect(self.reset_backup_location)
        loc_row.addWidget(reset_backup_btn)
        backup_layout.addLayout(loc_row)
        
        # Horizontal Separator
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        backup_layout.addWidget(line)
        
        # Manual Actions Grid
        actions_grid = QGridLayout()
        
        # Backup Config
        self.btn_backup_cfg = QPushButton(STRINGS["btn_backup_config"])
        self.btn_backup_cfg.clicked.connect(self.do_backup_config)
        actions_grid.addWidget(self.btn_backup_cfg, 0, 0)
        
        # Backup Data
        self.btn_backup_data = QPushButton(STRINGS["btn_backup_data"])
        self.btn_backup_data.clicked.connect(self.do_backup_data)
        actions_grid.addWidget(self.btn_backup_data, 0, 1)
        
        # Restore Config
        self.btn_restore_cfg = QPushButton(STRINGS["btn_restore_config"])
        self.btn_restore_cfg.clicked.connect(self.do_restore_config)
        
        if self.theme_manager:
            warning_color = self.theme_manager.get_palette()['warning']
            w_contrast = self.theme_manager.get_contrast_color(warning_color)
            self.btn_restore_cfg.setStyleSheet(f"background-color: {warning_color}; color: {w_contrast};")
        actions_grid.addWidget(self.btn_restore_cfg, 1, 0)
        
        # Restore Data
        self.btn_restore_data = QPushButton(STRINGS["btn_restore_data"])
        self.btn_restore_data.clicked.connect(self.do_restore_data)
        self.btn_restore_data.setStyleSheet(f"background-color: {warning_color}; color: {w_contrast};")
        actions_grid.addWidget(self.btn_restore_data, 1, 1)
        
        backup_layout.addLayout(actions_grid)
        backup_group.setLayout(backup_layout)
        form_layout.addRow(backup_group)

        # 2. Data File Path
        path_group = QGroupBox(STRINGS["data_file_group_title"])
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit(data_manager.data_file)
        self.path_input.setReadOnly(True)
        path_layout.addWidget(self.path_input)
        browse_button = QPushButton(STRINGS["browse_button"])
        browse_button.clicked.connect(self.browse_file)
        path_layout.addWidget(browse_button)
        path_group.setLayout(path_layout)
        form_layout.addRow(path_group)

        # 2. Appearance & General
        general_group = QGroupBox(STRINGS["group_general_settings"])
        general_layout = QVBoxLayout()
        
        # Appearance
        aesthetics_group = QGroupBox(STRINGS["group_aesthetics"])
        app_layout = QFormLayout()
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['Dark', 'Light', 'Neon Night', 'Nordic Forest', 'Pride', 'Trans Pride'])
        current_theme = config.get('theme', 'Dark')
        self.theme_combo.setCurrentText(current_theme)
        app_layout.addRow("Theme:", self.theme_combo)
        
        # Custom Accent
        accent_row = QHBoxLayout()
        self.accent_color_preview = QPushButton()
        self.accent_color_preview.setFixedSize(24, 24)
        current_accent = config.get('accent_color', '#6200ea')
        self.current_accent_hex = current_accent
        self.update_accent_preview(current_accent)
        accent_row.addWidget(self.accent_color_preview)
        
        pick_accent_btn = QPushButton(STRINGS["btn_pick_color"])
        pick_accent_btn.clicked.connect(self.pick_custom_accent)
        accent_row.addWidget(pick_accent_btn)
        accent_row.addStretch()
        app_layout.addRow("Accent Color:", accent_row)
        
        aesthetics_group.setLayout(app_layout)
        general_layout.addWidget(aesthetics_group)
        self.start_boot_chk = QCheckBox(STRINGS["chk_start_windows"])
        self.start_boot_chk.setChecked(self.is_run_on_startup())
        general_layout.addWidget(self.start_boot_chk)
        
        self.tray_chk = QCheckBox(STRINGS["chk_minimize_tray"])
        self.tray_chk.setChecked(config.get('minimize_to_tray', True))
        general_layout.addWidget(self.tray_chk)

        # Reminder Days
        reminder_row = QHBoxLayout()
        self.reminder_days_spin = QSpinBox()
        self.reminder_days_spin.setRange(0, 30)
        self.reminder_days_spin.setValue(config.get('reminder_days', 1))
        self.reminder_days_spin.setSuffix(STRINGS["suffix_days_advance"])
        reminder_row.addWidget(QLabel(STRINGS["label_notify_me"]))
        reminder_row.addWidget(self.reminder_days_spin)
        general_layout.addLayout(reminder_row)
        
        general_group.setLayout(general_layout)
        form_layout.addRow(general_group)

        # 3. Language Selection
        lang_group = QGroupBox(STRINGS["lang_group_title"])
        lang_layout = QHBoxLayout()
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(list(TRANSLATIONS.keys()))
        current_lang = config.get('language', 'English')
        self.lang_combo.setCurrentText(current_lang)
        lang_layout.addWidget(QLabel(STRINGS["lang_group_title"] + ":"))
        lang_layout.addWidget(self.lang_combo)
        lang_group.setLayout(lang_layout)
        form_layout.addRow(lang_group)

        # 4. Notifications (v6.2.0)
        notif_group = QGroupBox(STRINGS["group_notif_settings"])
        notif_layout = QVBoxLayout()

        self.webhook_chk = QCheckBox(STRINGS["chk_enable_webhooks"])
        self.webhook_chk.setChecked(config.get('webhooks_enabled', False))
        notif_layout.addWidget(self.webhook_chk)

        webhook_row = QFormLayout()
        self.webhook_input = QLineEdit(config.get('webhook_url', ''))
        webhook_row.addRow(STRINGS["lbl_webhook_url"] + ":", self.webhook_input)

        self.reminder_time_input = QLineEdit(config.get('reminder_time', '09:00'))
        self.reminder_time_input.setPlaceholderText("HH:MM")
        webhook_row.addRow(STRINGS["lbl_reminder_time"] + ":", self.reminder_time_input)
        notif_layout.addLayout(webhook_row)

        test_btn = QPushButton(STRINGS["btn_test_webhook"])
        test_btn.clicked.connect(self.test_webhook)
        notif_layout.addWidget(test_btn)

        notif_group.setLayout(notif_layout)
        form_layout.addRow(notif_group)

        # 5. Security (PIN Protection) 🛡️
        pin_group = QGroupBox(STRINGS["group_security_pin"])
        pin_layout = QVBoxLayout()
        self.pin_chk = QCheckBox(STRINGS["chk_enable_pin"])
        # Fix: Read from security metadata (authoritative), not config
        self.pin_chk.setChecked(self.data_manager.security.get('pin_enabled', False))
        pin_layout.addWidget(self.pin_chk)
        self.set_pin_btn = QPushButton(STRINGS["btn_set_change_pin"])
        self.set_pin_btn.clicked.connect(self.setup_pin)
        pin_layout.addWidget(self.set_pin_btn)
        pin_group.setLayout(pin_layout)
        form_layout.addRow(pin_group)
        
        # Auto-lock settings (only shown if PIN is enabled)
        autolock_group = QGroupBox("🔒 " + STRINGS["chk_auto_lock"])
        autolock_layout = QVBoxLayout()
        self.auto_lock_chk = QCheckBox(STRINGS["chk_auto_lock"])
        self.auto_lock_chk.setChecked(config.get('auto_lock_enabled', False))
        autolock_layout.addWidget(self.auto_lock_chk)
        
        self.lock_min_chk = QCheckBox(STRINGS["chk_lock_on_minimize"])
        self.lock_min_chk.setChecked(config.get('lock_on_minimize', False))
        autolock_layout.addWidget(self.lock_min_chk)
        
        timeout_layout = QHBoxLayout()
        timeout_layout.addWidget(QLabel(STRINGS["label_idle_timeout"] + ":"))
        self.idle_timeout_spin = QSpinBox()
        self.idle_timeout_spin.setRange(1, 60)
        self.idle_timeout_spin.setValue(config.get('idle_timeout_minutes', 5))
        self.idle_timeout_spin.setSuffix(STRINGS["suffix_minutes"])
        timeout_layout.addWidget(self.idle_timeout_spin)
        timeout_layout.addStretch()
        autolock_layout.addLayout(timeout_layout)
        autolock_group.setLayout(autolock_layout)
        form_layout.addRow(autolock_group)

        # 5. Cloud Sync ☁️
        cloud_group = QGroupBox(STRINGS["group_cloud_sync"])
        sync_layout = QVBoxLayout()
        sync_path_layout = QHBoxLayout()
        self.sync_path_input = QLineEdit(config.get('sync_path', ''))
        self.sync_path_input.setPlaceholderText("Select Cloud Folder (OneDrive, Dropbox, etc.)")
        sync_path_layout.addWidget(self.sync_path_input)
        browse_sync_btn = QPushButton(STRINGS["browse_button"])
        browse_sync_btn.clicked.connect(self.browse_sync_folder)
        sync_path_layout.addWidget(browse_sync_btn)
        sync_layout.addLayout(sync_path_layout)
        cloud_label = QLabel(STRINGS["lbl_cloud_sync_desc"])
        if self.theme_manager:
            p = self.theme_manager.get_palette()
            cloud_label.setStyleSheet(f"font-size: 9pt; color: {p['text_secondary']};")
        sync_layout.addWidget(cloud_label)
        cloud_group.setLayout(sync_layout)
        form_layout.addRow(cloud_group)

        # 6. Backup Manager
        backup_group = QGroupBox(STRINGS["group_backup_restore"])
        backup_layout = QVBoxLayout()
        self.backup_list = QListWidget()
        self.backup_list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.backup_list.setFixedHeight(100)
        self.load_backups()
        backup_layout.addWidget(self.backup_list)
        btn_layout = QHBoxLayout()
        create_backup_btn = QPushButton(STRINGS["btn_create_backup"])
        create_backup_btn.clicked.connect(self.create_manual_backup)
        btn_layout.addWidget(create_backup_btn)
        restore_btn = QPushButton(STRINGS["btn_restore_selected"])
        restore_btn.clicked.connect(self.restore_selected_backup)
        btn_layout.addWidget(restore_btn)
        delete_btn = QPushButton(STRINGS["btn_delete_selected"])
        delete_btn.clicked.connect(self.delete_selected_backup)
        btn_layout.addWidget(delete_btn)
        backup_layout.addLayout(btn_layout)
        backup_group.setLayout(backup_layout)
        form_layout.addRow(backup_group)

        # 7. Danger Zone
        danger_group = QGroupBox(STRINGS["group_danger_zone"])
        danger_layout = QVBoxLayout()
        clear_btn = QPushButton(STRINGS["btn_clear_all_data"])
        if self.theme_manager:
            p = self.theme_manager.get_palette()
            danger_color = p['danger']
            d_contrast = self.theme_manager.get_contrast_color(danger_color)
            clear_btn.setStyleSheet(f"background-color: {danger_color}; color: {d_contrast}; font-weight: bold;")
        clear_btn.clicked.connect(self.clear_all_data)
        danger_layout.addWidget(clear_btn)
        
        # Factory Reset (Delete Configs)
        reset_btn = QPushButton(STRINGS["btn_factory_reset_full"])
        # Use danger color for reset as well
        reset_btn.setStyleSheet(f"background-color: {danger_color}; color: {d_contrast}; font-weight: bold;")
        reset_btn.clicked.connect(self.factory_reset)
        danger_layout.addWidget(reset_btn)
        
        danger_group.setLayout(danger_layout)
        form_layout.addRow(danger_group)


        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # 8. Action Buttons (Bottom)
        bottom_layout = QHBoxLayout()
        save_button = QPushButton(STRINGS["btn_save_settings"])
        if self.theme_manager:
            p = self.theme_manager.get_palette()
            success_color = p['success']
            s_contrast = self.theme_manager.get_contrast_color(success_color)
            save_button.setStyleSheet(f"background-color: {success_color}; color: {s_contrast}; font-weight: bold; padding: 8px;")
        save_button.clicked.connect(self.save_settings)
        bottom_layout.addStretch()
        bottom_layout.addWidget(save_button)
        cancel_btn = QPushButton(STRINGS["btn_cancel"])
        cancel_btn.clicked.connect(self.reject)
        bottom_layout.addWidget(cancel_btn)
        layout.addLayout(bottom_layout)
        
        self.setLayout(layout)

    def load_backups(self):
        self.backup_list.clear()
        backup_dir = os.path.join(self.data_manager.config_dir, 'backups')
        if os.path.exists(backup_dir):
            backups = sorted([f for f in os.listdir(backup_dir) if f.startswith('bill_data_')])
            self.backup_list.addItems(backups)
            
    def create_manual_backup(self):
        try:
            self.data_manager.backup_data()
            self.load_backups()
            QMessageBox.information(self, STRINGS["title_backup_created"], STRINGS["msg_backup_created"])
        except Exception as e:
            QMessageBox.critical(self, STRINGS["title_error"], STRINGS["msg_backup_failed"].format(e))
            
    def restore_selected_backup(self):
        selected_items = self.backup_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, STRINGS["title_selection_required"], STRINGS["msg_select_backup"])
            return

        if len(selected_items) > 1:
            QMessageBox.warning(self, STRINGS["title_selection_required"], STRINGS["msg_select_single_restore"])
            return
            
        filename = selected_items[0].text()
        backup_path = os.path.join(self.data_manager.config_dir, 'backups', filename)
        
        reply = QMessageBox.question(self, STRINGS["title_confirm_restore"], 
                                   STRINGS["msg_confirm_restore"].format(filename),
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                shutil.copy2(backup_path, self.data_manager.data_file)
                QMessageBox.information(self, STRINGS["title_restored"], STRINGS["msg_restored"])
                if hasattr(self.parent(), 'load_data'):
                    self.parent().load_data()
                    self.parent().update_display()
            except Exception as e:
                QMessageBox.critical(self, STRINGS["title_restore_failed"], STRINGS["msg_restore_error"].format(e))

    def delete_selected_backup(self):
        selected_items = self.backup_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, STRINGS["title_selection_required"], STRINGS["msg_select_backup"])
            return
            
        count = len(selected_items)
        if count == 1:
            confirm_msg = STRINGS["msg_confirm_delete_backup"].format(selected_items[0].text())
        else:
            confirm_msg = STRINGS["msg_confirm_delete_backup_batch"].format(count)
            
        reply = QMessageBox.question(self, STRINGS["title_confirm_delete_backup"], 
                                   confirm_msg,
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                deleted_count = 0
                for item in selected_items:
                    filename = item.text()
                    backup_path = os.path.join(self.data_manager.config_dir, 'backups', filename)
                    if os.path.exists(backup_path):
                        os.remove(backup_path)
                        deleted_count += 1
                
                QMessageBox.information(self, STRINGS["title_data_cleared"], STRINGS["msg_batch_delete_success"].format(deleted_count))
                self.load_backups()
            except Exception as e:
                logging.error(f"Failed to delete backup: {e}")
                QMessageBox.critical(self, STRINGS["title_error"], f"Error: {e}")

    def clear_all_data(self):
        """Clear all application data."""
        reply = QMessageBox.question(self, STRINGS["title_clear_all_data"], 
                                   STRINGS["msg_confirm_clear_1"],
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            confirm = QMessageBox.question(self, STRINGS["title_double_confirm"], 
                                         STRINGS["msg_confirm_clear_2"],
                                          QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                try:
                    # Create a backup first just in case
                    self.data_manager.backup_data()
                    
                    # Reset data
                    empty_data = {
                        "budget": 0.0,
                        "unpaid_bills": [],
                        "paid_bills": [],
                        "budget_currency": "$ (USD)",
                        "bill_currency": "$ (USD)",
                        "summary_currency": "$ (USD)"
                    }
                    self.data_manager.save_data(empty_data)
                    QMessageBox.information(self, STRINGS["title_data_cleared"], STRINGS["msg_data_cleared_restart"])
                    if hasattr(self.parent(), 'load_data'):
                        self.parent().load_data()
                        self.parent().update_display()
                except Exception as e:
                    QMessageBox.critical(self, STRINGS["title_error"], f"Failed to clear data: {e}")
    
    def factory_reset(self):
        """Delete all configuration and data files."""
        warning = QMessageBox(self)
        warning.setWindowTitle(STRINGS["title_factory_reset"])
        warning.setText(STRINGS["msg_factory_reset_warning"])
        warning.setIcon(QMessageBox.Icon.Critical)
        warning.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        warning.setDefaultButton(QMessageBox.StandardButton.No)
        
        if warning.exec() == QMessageBox.StandardButton.Yes:
            input_dialog = QInputDialog(self)
            input_dialog.setWindowTitle(STRINGS["title_confirm_reset"])
            input_dialog.setLabelText(STRINGS["msg_type_delete"])
            if input_dialog.exec() == QDialog.DialogCode.Accepted and input_dialog.textValue() == "DELETE":
                try:
                    logging.shutdown() # Release log file lock
                    config_dir = self.data_manager.config_dir
                    if os.path.exists(config_dir):
                        # Attempt to remove everything
                        for filename in os.listdir(config_dir):
                            file_path = os.path.join(config_dir, filename)
                            try:
                                if os.path.isfile(file_path) or os.path.islink(file_path):
                                    os.unlink(file_path)
                                elif os.path.isdir(file_path):
                                    shutil.rmtree(file_path)
                            except Exception as e:
                                print(f"Failed to delete {file_path}. Reason: {e}")
                                
                    QMessageBox.information(self, STRINGS["title_reset_complete"], STRINGS["msg_reset_success_close"])
                    QApplication.quit()
                except Exception as e:
                     QMessageBox.critical(self, STRINGS["title_error"], f"Reset failed: {e}")

    def browse_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Choose data file", "", "JSON Files (*.json)")
        if file_path:
            self.path_input.setText(file_path)
            # We don't save immediately here to allow 'Save' button to handle everything
            
    def save_settings(self):
        # 1. Save Data Path (with validation)
        new_path = self.path_input.text()
        if new_path and new_path != self.data_manager.data_file:
            # Validate path for security
            if not validate_file_path(new_path):
                QMessageBox.warning(self, STRINGS["title_invalid_path"], STRINGS["msg_invalid_path_security"])
                return
            
            self.data_manager.data_file = new_path
            # We update config immediately for path
            pin = self.parent().session_pin if hasattr(self.parent(), 'session_pin') else None
            path_config = self.data_manager.load_config(pin)
            path_config['data_file_path'] = new_path
            self.data_manager.save_config(path_config, pin)

        # 2. Update Main Config (Tray, Reminder, Language, Sync Path)
        pin = self.parent().session_pin if hasattr(self.parent(), 'session_pin') else None
        config = self.data_manager.load_config(pin)
        config['minimize_to_tray'] = self.tray_chk.isChecked()
        config['reminder_days'] = self.reminder_days_spin.value()
        # Cloud Sync
        config['sync_path'] = self.sync_path_input.text()
        
        # Backup Location
        config['backup_dir'] = self.backup_path_input.text()
        
        # Handle Language Change
        selected_lang = self.lang_combo.currentText()
        if selected_lang != config.get('language', 'English'):
            config['language'] = selected_lang
            QMessageBox.information(self, STRINGS["title_restart_required"], STRINGS["lang_restart_msg"])
            
        # Aesthetics Series (v6.5.0)
        config['theme'] = self.theme_combo.currentText()
        config['accent_color'] = self.current_accent_hex
        
        # Apply theme immediately to main window if changed
        if hasattr(self.parent(), 'theme_manager'):
            self.parent().theme_manager.set_theme(config['theme'])
            self.parent().theme_manager.set_accent(config['accent_color'])
            set_theme(self.parent().theme_manager)
            
        # Update Security Metadata (security.json)
        pin_enabled = self.pin_chk.isChecked()
        self.data_manager.security['pin_enabled'] = pin_enabled
        self.data_manager.save_security()

        if self.auto_lock_chk.isChecked() != config.get('auto_lock_enabled', False):
            config['auto_lock_enabled'] = self.auto_lock_chk.isChecked()
            
        config['lock_on_minimize'] = self.lock_min_chk.isChecked()
        config['idle_timeout_minutes'] = self.idle_timeout_spin.value()
        

        # v6.2.0 Notification Settings
        config['webhooks_enabled'] = self.webhook_chk.isChecked()
        config['webhook_url'] = self.webhook_input.text().strip()
        config['reminder_time'] = self.reminder_time_input.text().strip()
        
        # Save Config
        self.data_manager.save_config(config, self.session_pin)

        # 3. Save Registry (Startup)
        try:
            self.set_run_on_startup(self.start_boot_chk.isChecked())
        except PermissionError:
            QMessageBox.warning(self, STRINGS["title_permission_denied"], STRINGS["msg_admin_rights_required"])
        except Exception as e:
            QMessageBox.critical(self, STRINGS["title_error"], 
                f"Failed to update startup settings: {str(e)}")
        
        self.accept()

    def browse_backup_location(self):
        folder = QFileDialog.getExistingDirectory(self, STRINGS["lbl_backup_location"])
        if folder:
            self.backup_path_input.setText(folder)
            
    def reset_backup_location(self):
        default_path = os.path.join(self.data_manager.config_dir, 'backups')
        self.backup_path_input.setText(default_path)

    def do_backup_config(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        default_name = f"config_backup_{timestamp}.json"
        target, _ = QFileDialog.getSaveFileName(self, STRINGS["title_backup_config"], default_name, "JSON Files (*.json)")
        if target:
            if self.data_manager.backup_config(target):
                QMessageBox.information(self, STRINGS["title_success"], STRINGS["msg_backup_success"])
            else:
                QMessageBox.critical(self, STRINGS["title_error"], STRINGS["msg_backup_failed"])

    def do_backup_data(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        default_name = f"bill_data_backup_{timestamp}.json"
        target, _ = QFileDialog.getSaveFileName(self, STRINGS["title_backup_data"], default_name, "JSON Files (*.json)")
        if target:
            if not os.path.exists(self.data_manager.data_file):
                return
            try:
                shutil.copy2(self.data_manager.data_file, target)
                QMessageBox.information(self, STRINGS["title_success"], STRINGS["msg_backup_success"])
            except Exception as e:
                QMessageBox.critical(self, STRINGS["title_error"], STRINGS["msg_backup_failed"].format(e))

    def do_restore_config(self):
        warning = QMessageBox.warning(self, STRINGS["title_restore_config"], 
                                    STRINGS["msg_restore_warning"], 
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if warning == QMessageBox.StandardButton.Yes:
            source, _ = QFileDialog.getOpenFileName(self, STRINGS["title_restore_config"], "", "JSON Files (*.json);;All Files (*)")
            if source:
                if self.data_manager.restore_file(source, 'config'):
                    QMessageBox.information(self, STRINGS["title_restored"], STRINGS["msg_restart_required"])
                else:
                    QMessageBox.critical(self, STRINGS["title_error"], STRINGS["msg_restore_failed"])

    def do_restore_data(self):
        warning = QMessageBox.warning(self, STRINGS["title_restore_data"], 
                                    STRINGS["msg_restore_warning"], 
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if warning == QMessageBox.StandardButton.Yes:
            source, _ = QFileDialog.getOpenFileName(self, STRINGS["title_restore_data"], "", "JSON Files (*.json);;All Files (*)")
            if source:
                if self.data_manager.restore_file(source, 'data'):
                    QMessageBox.information(self, STRINGS["title_restored"], STRINGS["msg_data_restored_reload"])
                    if isinstance(self.parent(), BillTrackerWindow):
                        self.parent().load_data()
                        self.parent().update_display()
                else:
                    QMessageBox.critical(self, STRINGS["title_error"], STRINGS["msg_restore_failed"])

    def setup_pin(self):
        """Open dialog to set or change PIN."""
        dialog = PinEntryDialog(self, mode='set')
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_pin = dialog.pin_input.text().strip()
            if len(new_pin) < 4:
                QMessageBox.warning(self, STRINGS["title_invalid_pin"], STRINGS["msg_pin_too_short"])
                return
            
            # Get current session PIN (for loading encrypted config)
            current_pin = self.parent().session_pin if hasattr(self.parent(), 'session_pin') else None
            
            # Update security metadata (ALWAYS UNENCRYPTED)
            self.data_manager.security['pin_enabled'] = True
            self.data_manager.security['pin_hash'] = dialog.get_pin_hash()
            self.data_manager.security['pin_hint'] = dialog.get_pin_hint()
            self.data_manager.save_security()
            
            # Update config (Config file stays as is, just re-saved with new PIN key)
            config = self.data_manager.load_config(current_pin)
            self.data_manager.save_config(config, new_pin)
            
            # Update session pin for the current session
            if hasattr(self.parent(), 'session_pin'):
                self.parent().session_pin = new_pin
                
            self.pin_chk.setChecked(True)
            QMessageBox.information(self, STRINGS["title_success"], STRINGS["msg_pin_set_enabled"])

    def browse_sync_folder(self):
        """Open directory picker for cloud sync."""
        dir_path = QFileDialog.getExistingDirectory(self, "Select Cloud Sync Folder")
        if dir_path:
            self.sync_path_input.setText(dir_path)

    def pick_custom_accent(self):
        """Open color picker for custom accent color."""
        from PyQt6.QtWidgets import QColorDialog
        color = QColorDialog.getColor(QColor(self.current_accent_hex), self, "Pick Accent Color")
        if color.isValid():
            hex_color = color.name()
            self.current_accent_hex = hex_color
            self.update_accent_preview(hex_color)
            
    def update_accent_preview(self, hex_color):
        """Update the small color preview button."""
        self.accent_color_preview.setStyleSheet(f"background-color: {hex_color}; border: 1px solid white; border-radius: 12px;")

    def test_webhook(self):
        url = self.webhook_input.text().strip()
        if not url: return
        
        try:
            import json
            import urllib.request
            data = json.dumps({"content": "🔔 BillTracker Webhook Test: Connection Successful!"}).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                if response.getcode() in [200, 204]:
                    QMessageBox.information(self, STRINGS["title_success"], STRINGS["msg_webhook_test_sent"])
                else:
                    raise Exception(f"HTTP {response.getcode()}")
        except Exception as e:
            QMessageBox.critical(self, STRINGS["title_error"], STRINGS["msg_webhook_error"].format(str(e)))

    def is_run_on_startup(self):
        """Check if app runs on startup (cross-platform)."""
        system = platform.system()
        
        if system == 'Windows':
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
                winreg.QueryValueEx(key, "BillTracker")
                key.Close()
                return True
            except FileNotFoundError:
                return False
            except Exception as e:
                logging.error(f"Registry check error: {e}")
                return False
            finally:
                try: key.Close()
                except: pass
        
        elif system == 'Darwin':  # macOS
            plist_path = os.path.expanduser('~/Library/LaunchAgents/com.grouvya.billtracker.plist')
            return os.path.exists(plist_path)
        
        elif system == 'Linux':
            desktop_path = os.path.expanduser('~/.config/autostart/billtracker.desktop')
            return os.path.exists(desktop_path)
        
        return False

    def set_run_on_startup(self, enable):
        """Set app to run on startup (cross-platform)."""
        system = platform.system()
        
        if system == 'Windows':
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
                try:
                    if enable:
                        app_path = sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]
                        winreg.SetValueEx(key, "BillTracker", 0, winreg.REG_SZ, app_path)
                    else:
                        try:
                            winreg.DeleteValue(key, "BillTracker")
                        except FileNotFoundError:
                            pass
                finally:
                    key.Close()
            except Exception as e:
                logging.error(f"Registry write error: {e}")
        
        elif system == 'Darwin':  # macOS
            plist_dir = os.path.expanduser('~/Library/LaunchAgents')
            plist_path = os.path.join(plist_dir, 'com.grouvya.billtracker.plist')
            
            if enable:
                os.makedirs(plist_dir, exist_ok=True)
                app_path = sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]
                plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.grouvya.billtracker</string>
    <key>ProgramArguments</key>
    <array>
        <string>{app_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>'''
                try:
                    with open(plist_path, 'w') as f:
                        f.write(plist_content)
                except Exception as e:
                    logging.error(f"macOS startup file error: {e}")
            else:
                try:
                    if os.path.exists(plist_path):
                        os.remove(plist_path)
                except Exception as e:
                    logging.error(f"macOS startup file removal error: {e}")
        
        elif system == 'Linux':
            autostart_dir = os.path.expanduser('~/.config/autostart')
            desktop_path = os.path.join(autostart_dir, 'billtracker.desktop')
            
            if enable:
                os.makedirs(autostart_dir, exist_ok=True)
                app_path = sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]
                desktop_content = f'''[Desktop Entry]
Type=Application
Name=BillTracker
Exec={app_path}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Comment=Personal Finance Manager'''
                try:
                    with open(desktop_path, 'w') as f:
                        f.write(desktop_content)
                    os.chmod(desktop_path, 0o755)  # Make executable
                except Exception as e:
                    logging.error(f"Linux startup file error: {e}")
            else:
                try:
                    if os.path.exists(desktop_path):
                        os.remove(desktop_path)
                except Exception as e:
                    logging.error(f"Linux startup file removal error: {e}")




class ChartWidget(QWidget):
    """Simple Pie Chart Widget."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = {} # label: value
        self.colors = [
            QColor("#3a86ff"), QColor("#ff006e"), QColor("#8338ec"), 
            QColor("#fb5607"), QColor("#ffbe0b"), QColor("#3a0ca3"),
            QColor("#17c3b2"), QColor("#e63946")
        ]
        self.setMinimumSize(300, 300)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        save_action = menu.addAction(STRINGS["legend_save_image"])
        action = menu.exec(event.globalPos())
        if action == save_action:
            self.save_image()

    def save_image(self):
        file_path, _ = QFileDialog.getSaveFileName(self, STRINGS["title_save_chart"], "chart.png", "Images (*.png *.jpg *.bmp)")
        if file_path:
            pixmap = self.grab()
            pixmap.save(file_path)
            QMessageBox.information(self, STRINGS["title_saved"], STRINGS["msg_chart_saved"].format(file_path))

    def set_data(self, data):
        self.data = {k: v for k, v in data.items() if v > 0}
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Determine if dark mode via palette or just default text color
        # In QSS, text color is white/black. Let's check window text.
        is_dark = self.palette().color(QPalette.ColorRole.WindowText).lightness() > 128
        
        rect = self.rect()
        total = sum(self.data.values())
        if total == 0:
            painter.setPen(QColor("#888888"))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "No Data")
            return

        # Draw Pie
        start_angle = 90 * 16
        center = rect.center()
        radius = min(rect.width(), rect.height()) // 2 - 40
        pie_rect = QRectF(center.x() - radius, center.y() - radius, radius * 2, radius * 2)
        
        i = 0
        for label, value in self.data.items():
            span_angle = int((value / total) * 360 * 16)
            painter.setBrush(self.colors[i % len(self.colors)])
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawPie(pie_rect, start_angle, span_angle)
            start_angle -= span_angle # Move counter-clockwise
            i += 1
            
        # Legend (Simple)
        legend_y = 10
        painter.setPen(QColor("#ffffff") if is_dark else QColor("#000000"))
        i = 0
        for label, value in self.data.items():
            if legend_y > rect.height() - 20: break
            painter.setBrush(self.colors[i % len(self.colors)])
            painter.drawRect(10, legend_y, 10, 10)
            painter.drawText(25, legend_y + 10, f"{label}: {value:,.2f}")
            legend_y += 20
            i += 1


class TrendsWidget(QWidget):
    """Bar Chart for Spending History."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = {} # label: value
        self.setMinimumSize(300, 200)

    def set_data(self, data):
        self.data = data
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        
        is_dark = self.palette().color(QPalette.ColorRole.WindowText).lightness() > 128
        text_color = QColor("#ffffff") if is_dark else QColor("#000000")
        
        if not self.data:
            painter.setPen(QColor("#888888"))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "No History Data")
            return

        max_val = max(self.data.values()) if self.data else 1
        count = len(self.data)
        bar_width = (rect.width() - (count * 10)) / max(1, count)
        x = 5
        
        # Sort by date key (assuming YYYY-MM)
        sorted_keys = sorted(self.data.keys())[-6:] # Last 6 months
        
        for key in sorted_keys:
            val = self.data[key]
            h = (val / max_val) * (rect.height() - 40)
            
            # Bar
            painter.setBrush(self.palette().highlight().color())
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(int(x), int(rect.height() - h - 20), int(bar_width), int(h))
            
            # Label - safely extract month
            painter.setPen(text_color)
            parts = key.split('-')
            month_label = parts[1] if len(parts) >= 2 else key[:3]
            painter.drawText(QRect(int(x), int(rect.height() - 20), int(bar_width), 20), 
                           Qt.AlignmentFlag.AlignCenter, month_label)
            
            x += bar_width + 10

class BillCalendar(QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bills = [] # list of dicts

    def set_bills(self, bills):
        self.bills = bills
        self.updateCells()

    def paintCell(self, painter, rect, date):
        super().paintCell(painter, rect, date)
        dt = date.toString("yyyy-MM-dd")
        
        # Check for bills
        bills_on_day = [b for b in self.bills if b.get('due_date') == dt]
        if bills_on_day:
            painter.save()
            painter.setBrush(QColor(255, 0, 0, 50)) # Red tint
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(rect)
            
            # Small dot
            painter.setBrush(QColor("#ff0000"))
            painter.drawEllipse(rect.center(), 3, 3)
            painter.restore()

    def mouseDoubleClickEvent(self, event):
        """Handle double click to add a bill for the selected date."""
        self.activated.emit(self.selectedDate())
        super().mouseDoubleClickEvent(event)


class SplashScreen(QWidget):
    """Modern loading screen with progress indicator."""
    def __init__(self, accent_color='#8338ec'):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.SplashScreen | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(400, 250)
        
        # Center on screen
        screen = QApplication.primaryScreen().geometry()
        self.move((screen.width() - self.width()) // 2, (screen.height() - self.height()) // 2)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Background container
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 240);
                border-radius: 15px;
            }
        """)
        container_layout = QVBoxLayout()
        container_layout.setSpacing(20)
        
        # App logo/title
        user_accent = accent_color
        title = QLabel("💰 BillTracker")
        title.setStyleSheet(f"font-size: 36px; font-weight: bold; color: {user_accent}; background: transparent;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Version
        version = QLabel(f"v{__version__}")
        version.setStyleSheet("font-size: 14px; color: #aaaaaa; background: transparent;")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Loading message
        self.message = QLabel(STRINGS["msg_loading_config"])
        self.message.setStyleSheet("font-size: 14px; color: #ffffff; background: transparent;")
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 5px;
                background-color: rgba(255, 255, 255, 0.1);
                height: 8px;
            }}
            QProgressBar::chunk {{
                border-radius: 5px;
                background-color: {user_accent};
            }}
        """)
        
        container_layout.addWidget(title)
        container_layout.addWidget(version)
        container_layout.addWidget(self.message)
        container_layout.addWidget(self.progress)
        container.setLayout(container_layout)
        
        layout.addWidget(container)
        self.setLayout(layout)
    
    def update_progress(self, value, message=""):
        """Update progress bar and message."""
        self.progress.setValue(value)
        if message:
            self.message.setText(message)
        QApplication.processEvents()


def set_theme(theme_manager):
    """Apply QSS theme to the application using ThemeManager."""
    app = QApplication.instance()
    if not app:
        return

    app.setStyle("Fusion")
    app.setStyleSheet(theme_manager.get_stylesheet())


class LanguageSelectionDialog(QDialog):
    """First-run dialog to select the preferred language."""
    def __init__(self, accent_color='#6200ea', parent=None):
        super().__init__(parent)
        user_accent = accent_color
        self.setWindowTitle(STRINGS["title_language_selection"])
        self.setFixedSize(350, 200)
        self.selected_language = "English"  # Default
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        title = QLabel(STRINGS["label_first_run_title"])
        # Use same accent as splash title for consistency
        title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {user_accent};")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel(STRINGS["label_select_language"])
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["English", "Georgian"])
        layout.addWidget(self.lang_combo)
        
        start_btn = QPushButton(STRINGS["btn_start_app"])
        start_btn.clicked.connect(self.on_start)
        start_btn.setStyleSheet("font-weight: bold; padding: 5px;")
        layout.addWidget(start_btn)
        
        self.setLayout(layout)

    def on_start(self):
        self.selected_language = self.lang_combo.currentText()
        self.accept()



class BillCalendarWidget(QCalendarWidget):
    """Custom Calendar Widget to paint indicators for bills."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.daily_bills = {}  # Map date text -> list of (bill, type)

    def set_data(self, unpaid, paid):
        logging.warning("BillCalendarWidget: set_data called")
        self.daily_bills = {}
        
        def normalize_date(date_val):
            """Normalize various date formats to yyyy-MM-dd string."""
            if not date_val:
                return None
            try:
                # If it's already a QDate
                if isinstance(date_val, QDate):
                    return date_val.toString("yyyy-MM-dd")
                
                # If it's a string, try to parse it
                if isinstance(date_val, str):
                    # Try QDate parsing first
                    qdate = QDate.fromString(date_val, "yyyy-MM-dd")
                    if qdate.isValid():
                        return qdate.toString("yyyy-MM-dd")
                    
                    # Try other formats if needed, or simple string handling
                    # For now, let's assume if it's not yyyy-MM-dd it might need repair, 
                    # but if the app standardizes on yyyy-MM-dd we usually are good.
                    # Let's try ISO format fallback
                    try:
                        dt = datetime.fromisoformat(date_val).date()
                        return dt.strftime("%Y-%m-%d")
                    except ValueError:
                        pass
                        
                return str(date_val) # Fallback to original string
            except Exception:
                return str(date_val)

        for bill in unpaid:
            d = normalize_date(bill.get('due_date'))
            if d:
                self.daily_bills.setdefault(d, []).append(('unpaid', bill))
                logging.warning(f"BillCalendarWidget: Added unpaid bill on {d}")
        for bill in paid:
            raw_date = bill.get('paid_date', bill.get('due_date'))
            d = normalize_date(raw_date)
            if d:
                self.daily_bills.setdefault(d, []).append(('paid', bill))
                logging.warning(f"BillCalendarWidget: Added paid bill on {d}")
        
        logging.warning(f"BillCalendarWidget: Total daily_bills keys: {list(self.daily_bills.keys())}")
        self.update() # Trigger repaint of all cells

    def paintCell(self, painter, rect, date):
        super().paintCell(painter, rect, date)
        date_str = date.toString("yyyy-MM-dd")
        if date_str in self.daily_bills:
            logging.warning(f"BillCalendarWidget: Painting cell {date_str} - Found Data")
            bills = self.daily_bills[date_str]
            has_unpaid = any(b[0] == 'unpaid' for b in bills)
            has_paid = any(b[0] == 'paid' for b in bills)
            
            painter.save()
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Dot positions
            if has_unpaid:
                painter.setBrush(QColor(255, 85, 85)) # Red
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(rect.bottomRight() + QPoint(-15, -15), 6, 6)
            
            if has_paid:
                offset = -25 if has_unpaid else -15
                painter.setBrush(QColor(80, 250, 123)) # Green
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(rect.bottomRight() + QPoint(offset, -15), 6, 6)
                
            painter.restore()

class SubscriptionTab(QWidget):
    """A dedicated tab for managing recurring monthly subscriptions."""
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Burn Rate Header
        self.summary_card = QFrame()
        self.summary_card.setObjectName("SummaryCard")
        self.summary_card.setStyleSheet("QFrame#SummaryCard { background-color: rgba(98, 0, 234, 0.1); border-radius: 10px; padding: 15px; }")
        
        summary_layout = QVBoxLayout(self.summary_card)
        summary_layout.addWidget(QLabel(STRINGS["lbl_burn_rate"]))
        
        self.burn_rate_label = QLabel("0.00 USD")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.burn_rate_label.setFont(font)
        summary_layout.addWidget(self.burn_rate_label)

        self.yearly_burn_label = QLabel(f"{STRINGS['lbl_yearly']}: 0.00 USD")
        self.yearly_burn_label.setStyleSheet("opacity: 0.8; font-size: 11pt;")
        summary_layout.addWidget(self.yearly_burn_label)
        
        layout.addWidget(self.summary_card)
        
        # List of Subscriptions
        layout.addWidget(QLabel(STRINGS["tab_subscriptions"] + ":"))
        self.sub_list = QListWidget()
        self.sub_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.sub_list.customContextMenuRequested.connect(self.show_context_menu)
        
        # v6.3.5: Support left-click and double-click management
        self.sub_list.itemClicked.connect(lambda item: self.show_context_menu(self.sub_list.visualItemRect(item).center(), item))
        self.sub_list.itemDoubleClicked.connect(self.edit_subscription)
        
        layout.addWidget(self.sub_list)
        
        self.setLayout(layout)

    def show_context_menu(self, pos, item=None):
        if item is None:
            # Called from customContextMenuRequested (Right Click)
            item = self.sub_list.itemAt(pos)
        
        if not item:
            return
            
        menu = QMenu(self)
        
        edit_action = QAction(STRINGS["menu_edit_bill"], self)
        edit_action.triggered.connect(lambda: self.edit_subscription(item))
        menu.addAction(edit_action)
        
        delete_action = QAction(STRINGS["menu_delete_bill"], self)
        delete_action.triggered.connect(lambda: self.delete_subscription(item))
        menu.addAction(delete_action)
        
        # mapToGlobal(pos) works for both right-click pos and our calculated left-click center
        menu.exec(self.sub_list.mapToGlobal(pos))

    def edit_subscription(self, item):
        bill = item.data(Qt.ItemDataRole.UserRole)
        if not bill:
            return
        
        dialog = BillEditorDialog(self.main_window, bill, self.main_window.currencies)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = dialog.get_data()
            if new_data:
                # Update original object
                bill.update(new_data)
                self.main_window.save_data()
                self.main_window.update_display()

    def delete_subscription(self, item):
        bill = item.data(Qt.ItemDataRole.UserRole)
        if not bill:
            return
            
        confirm = QMessageBox.question(
            self, 
            STRINGS["menu_delete_bill"],
            STRINGS["msg_confirm_delete_history"].format(bill['name']) if bill in self.main_window.paid_bills else f"Delete '{bill['name']}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            if bill in self.main_window.unpaid_bills:
                self.main_window.unpaid_bills.remove(bill)
            elif bill in self.main_window.paid_bills:
                self.main_window.paid_bills.remove(bill)
            self.main_window.save_data()
            self.main_window.update_display()

    def refresh_data(self):
        self.sub_list.clear()
        
        # v6.7.0: Priority to is_subscription flag, fallback to recurring
        subscriptions = [b for b in self.main_window.unpaid_bills if b.get('is_subscription', False) or b.get('repeat_freq', 'No Repeat') != 'No Repeat']
        
        total_monthly_burn = 0.0
        # Sync with main window's summary currency preference
        target_curr = self.main_window.summary_currency_combo.currentText()
        if not target_curr:
            target_curr = "USD"
        
        # Extract code if needed ($ (USD) -> USD)
        import re
        curr_match = re.search(r'\((.*?)\)', target_curr)
        if curr_match:
            target_curr = curr_match.group(1)
            
        today = date.today()
        for sub in subscriptions:
            # Calculate monthly cost
            try:
                amount = float(sub['amount'])
            except (ValueError, TypeError):
                continue
                
            freq = sub.get('repeat_freq', 'No Repeat')
            
            # Normalize to Monthly
            if freq == 'Weekly':
                monthly_cost = amount * 4.33
            elif freq == 'Yearly':
                monthly_cost = amount / 12
            else: # Monthly or manual sub
                monthly_cost = amount
                
            # Convert to summary currency
            from_rate = self.main_window.exchange_rates.get(sub['currency'], 1.0)
            # Find target rate in exchange_rates dict (which uses codes usually, but check)
            # The exchange_rates dict keys are full names like "$ (USD)" in some places, 
            # let's find the correct key for target_curr code
            to_rate = 1.0
            for k, v in self.main_window.exchange_rates.items():
                if f"({target_curr})" in k:
                    to_rate = v
                    break
            
            if from_rate > 0:
                cost_converted = (monthly_cost / from_rate) * to_rate
                total_monthly_burn += cost_converted
            
            # Days until next payment
            try:
                due_date = datetime.strptime(sub['due_date'], '%Y-%m-%d').date()
                days_left = (due_date - today).days
                if days_left < 0:
                    days_str = STRINGS.get("lbl_overdue", "Overdue")
                elif days_left == 0:
                    days_str = STRINGS.get("lbl_due_today", "Due Today")
                else:
                    days_str = f"{days_left} {STRINGS['suffix_days_advance'].strip()}"
            except:
                days_str = ""

            # Display item
            metadata = self.main_window.currencies.get(sub['currency'], {'symbol': '$'})
            symbol = metadata.get('symbol', '$') if isinstance(metadata, dict) else metadata
            display_text = f"{sub['name']} - {symbol}{amount:,.2f} ({freq}) | {days_str}"
            
            # v6.3.2: Store bill object in item for editing/deletion
            item = QListWidgetItem(display_text)
            if days_str == STRINGS["lbl_due_today"] or days_str == STRINGS["lbl_overdue"]:
                item.setForeground(QColor("#ff5555")) # Alert color

            item.setData(Qt.ItemDataRole.UserRole, sub)
            self.sub_list.addItem(item)
            
        # Get symbol for target currency
        symbol_target = "$"
        for k, v in self.main_window.currencies.items():
            if f"({target_curr})" in k:
                symbol_target = v
                break
                
        self.burn_rate_label.setText(f"{symbol_target}{total_monthly_burn:,.2f}")
        self.yearly_burn_label.setText(f"{STRINGS['lbl_yearly_burn']}: {symbol_target}{total_monthly_burn * 12:,.2f}")


class CalendarTab(QWidget):
    """Tab showing interactive calendar."""
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.layout = QHBoxLayout()
        
        # Left: Calendar
        self.calendar = BillCalendarWidget()
        self.calendar.clicked.connect(self.on_date_click)
        self.layout.addWidget(self.calendar, 60)
        
        # Right: Details
        self.details_group = QGroupBox(STRINGS["label_due_on"].format(QDate.currentDate().toString(), ""))
        self.details_layout = QVBoxLayout()
        self.details_list = QListWidget()
        self.details_layout.addWidget(self.details_list)
        self.details_group.setLayout(self.details_layout)
        
        self.layout.addWidget(self.details_group, 40)
        self.setLayout(self.layout)
        
    def refresh_data(self):
        logging.warning("CalendarTab: refresh_data called")
        self.calendar.set_data(self.parent_window.unpaid_bills, self.parent_window.paid_bills)
        self.on_date_click(self.calendar.selectedDate())
        
    def on_date_click(self, qdate):
        date_str = qdate.toString("yyyy-MM-dd")
        # Format title safely
        try:
           base_title = STRINGS["label_due_on"]
           # We only start with one placeholder in standard text usually? 
           # Let's check the string definition: "Due on {}: {}" -> Format with date, ""
           title = base_title.format(date_str, "")
        except:
           title = f"Bills on {date_str}"
           
        self.details_group.setTitle(title)
        self.details_list.clear()
        
        bills = self.calendar.daily_bills.get(date_str, [])
        if not bills:
            try:
                msg = STRINGS.get("label_no_bills_due", "No bills due on {}").format(date_str)
            except:
                msg = f"No bills on {date_str}"
            self.details_list.addItem(msg)
            return
            
        for status, bill in bills:
            icon = "🔴" if status == 'unpaid' else "🟢"
            # Try to get symbol safely
            curr = bill.get('currency', 'USD')
            symbol = CURRENCY_SYMBOLS.get(curr, curr)
            item = QListWidgetItem(f"{icon} {bill['name']} - {symbol}{bill['amount']}")
            self.details_list.addItem(item)


class SearchDialog(QDialog):

    """Global search dialog for finding bills quickly."""
    def __init__(self, parent, unpaid_bills, paid_bills, currencies):
        super().__init__(parent)
        self.parent_window = parent
        self.unpaid_bills = unpaid_bills
        self.paid_bills = paid_bills
        self.currencies = currencies
        
        self.setWindowTitle(STRINGS["title_search"])
        self.setMinimumSize(700, 500)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Search Input
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(STRINGS["label_search_hint"])
        
        # Debounce timer to prevent lag during typing
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(lambda: self.perform_search(self.search_input.text()))
        
        # Connect to timer instead of direct search
        self.search_input.textChanged.connect(lambda: self.search_timer.start(300))  # 300ms delay
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Results Table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels([
            STRINGS["header_name"],
            STRINGS["header_amount"],
            STRINGS["header_category"],
            STRINGS["header_due_date"],
            STRINGS["header_status"]
        ])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.results_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.results_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.results_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.results_table.customContextMenuRequested.connect(self.show_context_menu)
        self.results_table.doubleClicked.connect(self.view_bill_details)
        layout.addWidget(self.results_table)
        
        # Initially show all bills
        self.perform_search("")
        
        # Focus on search input
        self.search_input.setFocus()
    
    def perform_search(self, query):
        """Filter and display bills based on search query."""
        query = query.lower().strip()
        
        # Combine unpaid and paid bills
        all_bills = []
        for bill in self.unpaid_bills:
            all_bills.append((bill, STRINGS["status_unpaid"]))
        for bill in self.paid_bills:
            all_bills.append((bill, STRINGS["status_paid"]))
        
        # Filter results
        results = []
        for bill, status in all_bills:
            if not query:
                results.append((bill, status))
            else:
                # Search in name, category, amount, date
                name_match = query in bill.get('name', '').lower()
                category_match = query in bill.get('category', '').lower()
                date_match = query in bill.get('due_date', '')
                amount_match = query in str(bill.get('amount', ''))
                
                if name_match or category_match or date_match or amount_match:
                    results.append((bill, status))
        
        # Display results
        self.results_table.setRowCount(len(results))
        for i, (bill, status) in enumerate(results):
            symbol_data = self.currencies.get(bill['currency'], '$')
            symbol = symbol_data.get('symbol', '$') if isinstance(symbol_data, dict) else symbol_data
            
            name_item = QTableWidgetItem(bill['name'])
            amount_item = QTableWidgetItem(f"{symbol}{bill['amount']:,.2f}")
            category_item = QTableWidgetItem(bill.get('category', 'Other'))
            date_item = QTableWidgetItem(bill.get('due_date', STRINGS["no_date_label"]))
            status_item = QTableWidgetItem(status)
            
            # Highlight overdue unpaid bills
            if status == STRINGS["status_unpaid"]:
                try:
                    due_dt = datetime.strptime(bill.get('due_date', ''), '%Y-%m-%d').date()
                    if due_dt < date.today():
                        for item in [name_item, amount_item, category_item, date_item, status_item]:
                            item.setForeground(QColor('#ff4d4d'))
                except:
                    pass
            
            self.results_table.setItem(i, 0, name_item)
            self.results_table.setItem(i, 1, amount_item)
            self.results_table.setItem(i, 2, category_item)
            self.results_table.setItem(i, 3, date_item)
            self.results_table.setItem(i, 4, status_item)
    
    def show_context_menu(self, position):
        """Show context menu for selected bill."""
        row = self.results_table.currentRow()
        if row < 0:
            return
        
        status = self.results_table.item(row, 4).text()
        menu = QMenu(self)
        
        if status == STRINGS["status_unpaid"]:
            pay_action = menu.addAction(STRINGS["menu_pay_bill"])
            pay_action.triggered.connect(lambda: self.pay_selected_bill(row))
            edit_action = menu.addAction(STRINGS["menu_edit_bill"])
            edit_action.triggered.connect(lambda: self.edit_selected_bill(row))
        
        view_action = menu.addAction(STRINGS["menu_view_details"])
        view_action.triggered.connect(lambda: self.view_bill_details())
        
        menu.exec(self.results_table.viewport().mapToGlobal(position))
    
    def get_bill_from_row(self, row):
        """Get the actual bill object from a table row."""
        name = self.results_table.item(row, 0).text()
        status = self.results_table.item(row, 4).text()
        
        bills_list = self.unpaid_bills if status == STRINGS["status_unpaid"] else self.paid_bills
        for bill in bills_list:
            if bill['name'] == name:
                return bill, status
        return None, None
    
    def pay_selected_bill(self, row):
        """Pay the selected bill."""
        bill, status = self.get_bill_from_row(row)
        if bill and status == STRINGS["status_unpaid"]:
            self.parent_window.pay_bill(bill)
            self.perform_search(self.search_input.text())  # Refresh results
    
    def edit_selected_bill(self, row):
        """Edit the selected bill."""
        bill, status = self.get_bill_from_row(row)
        if bill and status == STRINGS["status_unpaid"]:
            self.parent_window.edit_bill(bill)
            self.perform_search(self.search_input.text())  # Refresh results
    
    def view_bill_details(self):
        """Show bill details in a message box."""
        row = self.results_table.currentRow()
        if row < 0:
            return
        
        bill, status = self.get_bill_from_row(row)
        if not bill:
            return
        
        symbol_data = self.currencies.get(bill['currency'], '$')
        symbol = symbol_data.get('symbol', '$') if isinstance(symbol_data, dict) else symbol_data
        details = f"""
{STRINGS["header_name"]}: {bill['name']}
{STRINGS["header_amount"]}: {symbol}{bill['amount']:,.2f}
{STRINGS["header_category"]}: {bill.get('category', 'Other')}
{STRINGS["header_due_date"]}: {bill.get('due_date', STRINGS["no_date_label"])}
{STRINGS["header_frequency"]}: {bill.get('repeat_freq', 'No Repeat')}
{STRINGS["header_status"]}: {status}
"""
        QMessageBox.information(self, STRINGS["menu_view_details"], details.strip())



class PDFReportGenerator:
    """Generates PDF reports for the bill tracker."""
    def __init__(self, filename):
        self.filename = filename
        self.font_name = 'Helvetica'
        self.styles = getSampleStyleSheet()
        self.register_fonts()

    def register_fonts(self):
        """Register fonts that support Georgian characters."""
        try:
            # Try to register Sylfaen (standard on Windows for Georgian)
            font_path = "C:/Windows/Fonts/sylfaen.ttf"
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont('Sylfaen', font_path))
                self.font_name = 'Sylfaen'
            else:
                self.font_name = 'Helvetica' # Fallback
        except Exception as e:
            logging.warning(f"Failed to register font: {e}")
            self.font_name = 'Helvetica'

    def generate(self, summary_data, unpaid_bills, charts):
        """
        Generate the PDF report.
        summary_data: dict with 'total_unpaid', 'total_paid', 'budget', 'currency'
        unpaid_bills: list of bill dicts
        charts: list of temporary image paths
        """
        if not REPORTLAB_AVAILABLE:
            return False

        doc = SimpleDocTemplate(self.filename, pagesize=A4)
        elements = []
        
        # Styles
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=self.styles['Heading1'],
            fontName=self.font_name,
            fontSize=24,
            spaceAfter=20
        )
        
        normal_style = ParagraphStyle(
            'NormalCustom',
            parent=self.styles['Normal'],
            fontName=self.font_name,
            fontSize=10
        )
        
        header_style = ParagraphStyle(
            'HeaderCustom',
            parent=self.styles['Heading2'],
            fontName=self.font_name,
            fontSize=14,
            spaceAfter=10
        )

        # Title
        elements.append(Paragraph(f"{STRINGS['app_title']} - Report", title_style))
        elements.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", normal_style))
        elements.append(Spacer(1, 20))

        # 1. Summary Section
        elements.append(Paragraph("Financial Summary", header_style))
        
        currency = summary_data.get('currency', '$')
        data = [
            ["Metric", "Value"],
            ["Total Unpaid", f"{currency}{summary_data.get('total_unpaid', 0):,.2f}"],
            ["Total Paid (This Month)", f"{currency}{summary_data.get('total_paid', 0):,.2f}"],
            ["Monthly Budget", f"{currency}{summary_data.get('budget', 0):,.2f}"],
            ["Remaining Budget", f"{currency}{summary_data.get('remaining', 0):,.2f}"]
        ]
        
        t = Table(data, colWidths=[200, 200])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#6272a4')),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(t)
        elements.append(Spacer(1, 20))

        # 2. Charts
        if charts:
            elements.append(Paragraph("Visual Trends", header_style))
            for chart_path in charts:
                if os.path.exists(chart_path):
                    # Aspect ratio preservation could be added here
                    img = RLImage(chart_path, width=400, height=300) 
                    elements.append(img)
                    elements.append(Spacer(1, 10))
            elements.append(Spacer(1, 20))

        # 3. Unpaid Bills List
        if unpaid_bills:
            elements.append(Paragraph("Outstanding Bills", header_style))
            
            bill_data = [["Name", "Amount", "Due Date", "Category"]]
            for bill in unpaid_bills:
                sym = CURRENCY_SYMBOLS.get(bill.get('currency', 'USD'), '$')
                bill_data.append([
                    bill.get('name', ''),
                    f"{sym}{bill.get('amount', 0):,.2f}",
                    bill.get('due_date', ''),
                    bill.get('category', '')
                ])
            
            # Auto-wrap large tables? For now simple table
            bill_table = Table(bill_data, colWidths=[150, 100, 100, 150])
            bill_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff5555')), # Red header
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), self.font_name),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            elements.append(bill_table)

        try:
            doc.build(elements)
            return True
        except Exception as e:
            logging.error(f"PDF Generation failed: {e}")
            return False



class BillTrackerWindow(QMainWindow):
    """Main application window."""
    def get_exchange_rate(self, currency_code):
        """Robustly find exchange rate for a given currency code."""
        with self.data_lock:
            rates = self.exchange_rates
        
        # 1. Try direct code match
        if currency_code in rates:
            return rates[currency_code]
            
        # 2. Search by code in metadata
        for k, v in self.currencies.items():
            if isinstance(v, dict) and v.get('code') == currency_code:
                return rates.get(k, 1.0)
                
        return 1.0

    def __init__(self, session_pin=None):
        super().__init__()
        global STRINGS, CATEGORIES, FREQUENCIES
        self.session_pin = session_pin
        self.setWindowTitle(f"{STRINGS['app_title']} v{__version__}")
        self.setWindowIcon(QIcon(get_icon_path()))
        self.setGeometry(100, 100, 900, 1000)
        
        self.real_close = False # For minimize to tray mechanism
        
        # Apply 3% transparency
        self.setWindowOpacity(0.97)  # 3% transparent (97% opaque)
        
        # Initialize data
        config_dir = os.path.join(os.path.expanduser('~'), '.bill_tracker')
        self.data_manager = DataManager(config_dir)
        self.currencies = get_currency_list()
        
        self.unpaid_bills = []
        self.paid_bills = []
        self.budget = 0.0
        self.custom_categories = []
        self.savings_goals = []
        self.data_lock = threading.Lock() # Hardened: Protects shared data (rates, budget)
        
        # v6.3.6: Preferred currencies for dropdowns
        self.preferred_codes = ['USD', 'EUR', 'GEL', 'GBP', 'JPY', 'TRY', 'UAH', 'AMD', 'AZN', 'ILS']
        self.full_currency_list = self.get_filtered_currency_list()
        
        # Security: Brute-force protection
        self.failed_pin_attempts = 0
        self.lockout_until = None
        self.max_pin_attempts = 5
        self.lockout_duration = 300  # 5 minutes in seconds
        
        # Security: Auto-lock on idle
        self.idle_timer = None
        self.is_locked = False
        self.is_prompting = False
        self.idle_timeout_minutes = 5  # Default, will be loaded from config
        self.auto_lock_enabled = False  # Default, will be loaded from config
        self.lock_on_minimize = False   # Default, will be loaded from config
        self.last_activity_time = datetime.now()  # Initialize activity timestamp
        
        # Initialize exchange rates with safe defaults (1.0)
        self.exchange_rates = {curr: 1.0 for curr in self.currencies}
        
        self.load_data()
        
        # Load User Preferences (Theme, Language, etc.)
        # Pass session_pin to decrypt config now that we have it
        config = self.data_manager.load_config(session_pin)
        self.is_dark_mode = config.get('dark_mode', True)
        self.accent_color = config.get('accent_color', '#6200ea')
        
        # Initialize Theme Manager
        # Theme Persistence
        user_theme = config.get('theme', 'Dark')
        user_accent = config.get('accent_color', '#6200ea')
        
        self.theme_manager = ThemeManager()
        self.theme_manager.set_theme(user_theme)
        self.theme_manager.set_accent(user_accent)

        self.auto_lock_enabled = config.get('auto_lock_enabled', False)
        self.idle_timeout_minutes = config.get('idle_timeout_minutes', 5)
        self.lock_on_minimize = config.get('lock_on_minimize', False)
        self.minimize_to_tray = config.get('minimize_to_tray', False)
        
        # STARTUP LANGUAGE FIX: 
        # If config was encrypted, main() defaulted to English.
        # Now that we've decrypted it, reload the correct language.
        user_lang = config.get('language', 'English')
        if STRINGS.language != user_lang and user_lang in TRANSLATIONS:
            STRINGS = SafeStrings(user_lang)
            CATEGORIES = STRINGS["categories_list"]
            FREQUENCIES = STRINGS["frequencies_list"]
            
        # MIGRATION: Ensure language is synced to security metadata for next startup (PIN Dialog localization)
        if self.data_manager.security.get('language') != user_lang:
            config['language'] = user_lang
            self.data_manager.save_config(config, session_pin)
            CATEGORIES = STRINGS["categories_list"]
            FREQUENCIES = STRINGS["frequencies_list"]
            self.setWindowTitle(f"{STRINGS['app_title']} v{__version__}")
        
        # UI Setup

        # UI Setup
        # Suppress updates while building the UI to avoid repeated repaints
        self.setUpdatesEnabled(False)
        try:
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            main_layout = QVBoxLayout()
            central_widget.setLayout(main_layout)
            
            # Apply initial theme
            set_theme(self.theme_manager)
            
            # System Tray & Notifications
            self.tray_icon = QSystemTrayIcon(self)
            self.tray_icon.setIcon(QIcon(get_tray_icon_path()))
            
            # Tray Menu
            tray_menu = QMenu()
            open_action = tray_menu.addAction("Open")
            open_action.triggered.connect(self.show_window)
            quit_action = tray_menu.addAction("Quit")
            quit_action.triggered.connect(self.quit_app)
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.activated.connect(self.on_tray_activated)
            
            self.tray_icon.show()
            
            # Background Timer for Reminders (Every 30 minutes for higher precision on daily time)
            self.bg_timer = QTimer(self)
            self.bg_timer.timeout.connect(self.check_due_bills)
            self.bg_timer.start(1800000) # 30 minutes in ms
            
            # Check for due bills after a short delay
            QTimer.singleShot(2000, self.check_due_bills)

            # Tabs
            self.tabs = QTabWidget()
            main_layout.addWidget(self.tabs)
            
            # Connect tab change for lazy loading
            self.tabs.currentChanged.connect(self._on_tab_changed)
            
            # Chart cache for performance
            self._chart_cache_hash = None
            
            # Tab 1: Dashboard
            self.dashboard_tab = QWidget()
            self.setup_dashboard_tab()
            self.tabs.addTab(self.dashboard_tab, STRINGS["tab_dashboard"])
            
            # Tab 2: Unpaid Bills
            self.unpaid_tab = QWidget()
            self.setup_unpaid_tab()
            self.tabs.addTab(self.unpaid_tab, STRINGS["tab_unpaid"])
            
            # Tab 3: Paid History
            self.paid_tab = QWidget()
            self.setup_paid_tab()
            self.tabs.addTab(self.paid_tab, STRINGS["tab_paid"])

            # Tab 4: Charts
            self.chart_tab = QWidget()
            self.setup_chart_tab()
            self.tabs.addTab(self.chart_tab, STRINGS["tab_trends"])

            # Tab 5: Calendar
            self.calendar_tab = CalendarTab(self)
            self.tabs.addTab(self.calendar_tab, STRINGS["tab_calendar"])
            self.calendar_tab.refresh_data()

            # Tab 6: Subscriptions
            self.subscription_tab = SubscriptionTab(self)
            self.tabs.addTab(self.subscription_tab, STRINGS["tab_subscriptions"])

            # Tab 7: Savings Goals (v6.7.0)
            self.savings_tab = SavingsTab(self)
            self.tabs.addTab(self.savings_tab, STRINGS["tab_savings"])

            # Tab 8: About
            ma_about_text = STRINGS.get("tab_about", "ℹ️ About")
            self.about_tab = QWidget()
            self.setup_about_tab()
            self.tabs.addTab(self.about_tab, ma_about_text)
            
            # Initialize about tab lazy loading flag
            self.about_loaded = False

            # Final Initialization
            # Load cached rates and schedule fetching new ones shortly after startup
            cached = self.data_manager.load_rates_cache()
            if cached and isinstance(cached, dict) and 'conversion_rates' in cached:
                self.handle_api_result({'status': 'success', 'data': cached})

            # Delay the live refresh slightly so the UI becomes responsive first
            QTimer.singleShot(300, self.refresh_rates)
            QTimer.singleShot(50, self.update_display)
            
            # Timer for periodic rate refresh
            self.rate_timer = QTimer()
            self.rate_timer.timeout.connect(self.refresh_rates)
            
            # Performance: Debounce timer for filtering
            self.filter_timer = QTimer()
            self.filter_timer.setSingleShot(True)
            self.filter_timer.timeout.connect(self.update_unpaid_table_view)
            self.rate_timer.start(3600000)  # Every hour
            
            # Security: Idle timer for auto-lock
            self.idle_timer = QTimer()
            self.idle_timer.timeout.connect(self.check_idle_timeout)
            self.idle_timer.start(60000)  # Check every minute
            
            # Load auto-lock settings from config
            config = self.data_manager.load_config(self.session_pin)
            self.auto_lock_enabled = bool(config.get('auto_lock_enabled', False))
            try:
                self.idle_timeout_minutes = int(config.get('idle_timeout_minutes', 5))
            except (ValueError, TypeError):
                self.idle_timeout_minutes = 5
            
            # Connect combo boxes
            self.budget_currency_combo.currentTextChanged.connect(self.on_currency_changed)
            self.summary_currency_combo.currentTextChanged.connect(self.on_currency_changed)

            # Restore last used currencies
            self.restore_currency_preferences()

            # Keyboard Shortcuts
            search_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
            search_shortcut.activated.connect(self.open_search)
            
            quick_add_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
            quick_add_shortcut.activated.connect(self.quick_add_bill)

            # Install event filter for activity tracking (auto-lock)
            QApplication.instance().installEventFilter(self)
        except Exception as e:
            logging.error(f"UI initialization error: {e}")
            # Fallback: create at least a basic layout if everything fails
            if not self.centralWidget():
                self.setCentralWidget(QWidget())
        finally:
            # CRITICAL: Always re-enable updates to prevent blank window 🛡️
            self.setUpdatesEnabled(True)

    def get_filtered_currency_list(self):
        """Returns a dynamic list of currencies based on usage frequency (Top 5 + Active)."""
        all_display_keys = sorted(self.currencies.keys())
        
        # 1. Calculate Frequency
        frequency = {}
        
        # Helper to count
        def add_count(curr_str):
            if not curr_str: return
            frequency[curr_str] = frequency.get(curr_str, 0) + 1
            
        # Scan Bills
        for b in self.unpaid_bills + self.paid_bills:
            add_count(b.get('currency'))
            
        # Scan Savings Goals
        if hasattr(self, 'savings_goals'):
            for g in self.savings_goals:
                add_count(g.get('currency'))
                
        # 2. Identify Currently Active Currencies (Must always be present)
        active_currencies = set()
        
        # Budget
        if hasattr(self, 'budget_currency_combo'):
            active_currencies.add(self.budget_currency_combo.currentText())
            
        # Summary
        if hasattr(self, 'summary_currency_combo'):
            active_currencies.add(self.summary_currency_combo.currentText())
            
        # Bill (if we are in context of adding a bill, we might want to preserve its current state)
        if hasattr(self, 'bill_currency_combo'):
            active_currencies.add(self.bill_currency_combo.currentText())
            
        # 3. Sort by Frequency
        # Sort keys by count descending
        sorted_by_usage = sorted(frequency.keys(), key=lambda k: frequency[k], reverse=True)
        
        # Take Top 5
        top_5 = sorted_by_usage[:5]
        
        # 4. Construct Final List
        # Start with a base set of Top 5 + Active
        final_set = set(top_5)
        final_set.update(active_currencies)
        
        # 5. Fallback/Cold Start
        # If user has almost no data (e.g. < 2 currencies used/active), add some majors to prompt them.
        if len(final_set) < 2:
            default_majors = []
            # Find display keys for USD, EUR, GBP
            # We iterate all keys to find matches if we only know code
            needed_codes = ['USD', 'EUR', 'GBP']
            for k, meta in self.currencies.items():
                if meta['code'] in needed_codes:
                    default_majors.append(k)
            final_set.update(default_majors)
            
        # Filter None or empty
        final_set = {x for x in final_set if x}
        
        # Return sorted list (alphabetical for UI consistency within the short list? 
        # Or frequency? Usually dropdowns are alphabetical or frequency. 
        # User asked for "most frequent". But for a list of ~5 items, maybe frequency order is best?
        # Actually, let's sort by frequency order (Active/Top ones first) or just standard sort.
        # "Preferred Currencies" usually implies a set. 
        # Let's return them in the order: [Active] + [Top Frequent] + [Others if any]
        # But `sorted` is safest for UI prediction.
        # Let's sticking to alphabetical for the dropdown result to make it easy to scan.
        return sorted(list(final_set))

    def setup_dashboard_tab(self):
        layout = QVBoxLayout()
        self.dashboard_tab.setLayout(layout)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # Mini Mode Toggle (v6.2.0)
        mini_row = QHBoxLayout()
        mini_row.addStretch()
        self.btn_mini = QPushButton(STRINGS["btn_switch_mini"])
        self.btn_mini.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarNormalButton))
        self.btn_mini.clicked.connect(self.switch_to_mini_mode)
        mini_row.addWidget(self.btn_mini)
        
        self.btn_import = QPushButton(STRINGS["btn_import_csv"])
        self.btn_import.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon))
        self.btn_import.clicked.connect(self.import_bank_statement)
        mini_row.addWidget(self.btn_import)
        
        scroll_layout.addLayout(mini_row)
        
        # Budget section
        budget_group = QGroupBox(STRINGS["budget_group_title"])
        budget_layout = QHBoxLayout()
        self.budget_input = QLineEdit()
        budget_layout.addWidget(QLabel(STRINGS["budget_row_title"] + ":"))
        budget_layout.addWidget(self.budget_input)
        
        # Use lazy combo to avoid populating all currencies on startup
        self.budget_currency_combo = LazyCombo(items_provider=self.get_filtered_currency_list, pending_text=None)
        budget_layout.addWidget(self.budget_currency_combo)
        budget_search_btn = QPushButton("🔍 " + STRINGS["sort_name_button"])
        budget_search_btn.clicked.connect(lambda: self.open_currency_search(self.budget_currency_combo))
        budget_layout.addWidget(budget_search_btn)
        
        set_budget_btn = QPushButton(STRINGS["set_budget_button"])
        set_budget_btn.clicked.connect(self.set_budget)
        budget_layout.addWidget(set_budget_btn)
        budget_group.setLayout(budget_layout)
        scroll_layout.addWidget(budget_group)

        # Savings Progress Section (v6.7.0)
        self.savings_summary_group = QGroupBox(STRINGS["lbl_savings_goals"])
        savings_sum_layout = QVBoxLayout()
        
        self.dash_savings_progress = QProgressBar()
        self.dash_savings_progress.setRange(0, 100)
        p = self.theme_manager.get_palette()
        self.dash_savings_progress.setStyleSheet(f"QProgressBar {{ height: 20px; border: none; background-color: {p['surface']}; border: 1px solid {p['border']}; border-radius: 10px; text-align: center; color: {p['text']}; }} QProgressBar::chunk {{ background-color: {p['success']}; border-radius: 10px; }}")
        savings_sum_layout.addWidget(self.dash_savings_progress)
        
        self.dash_savings_stats = QLabel("0.00 / 0.00 USD")
        self.dash_savings_stats.setAlignment(Qt.AlignmentFlag.AlignCenter)
        savings_sum_layout.addWidget(self.dash_savings_stats)
        
        self.savings_summary_group.setLayout(savings_sum_layout)
        scroll_layout.addWidget(self.savings_summary_group)
        
        # Add Bill Section
        add_bill_group = QGroupBox(STRINGS["add_bill_group_title"])
        add_bill_layout = QGridLayout()
        
        self.bill_name_input = QLineEdit()
        add_bill_layout.addWidget(QLabel(STRINGS["bill_name_row"] + ":"), 0, 0)
        add_bill_layout.addWidget(self.bill_name_input, 0, 1)
        
        self.bill_amount_input = QLineEdit()
        add_bill_layout.addWidget(QLabel(STRINGS["amount_row"] + ":"), 1, 0)
        add_bill_layout.addWidget(self.bill_amount_input, 1, 1)
        
        # Currency Row with Search
        add_bill_layout.addWidget(QLabel(STRINGS["currency_label"] + ":"), 2, 0)
        curr_layout = QHBoxLayout()
        self.bill_currency_combo = LazyCombo(items_provider=self.get_filtered_currency_list, pending_text=None)
        self.bill_currency_combo.currentTextChanged.connect(self.on_currency_changed)
        curr_layout.addWidget(self.bill_currency_combo)
        curr_search_btn = QPushButton("🔍")
        curr_search_btn.setFixedWidth(40)
        curr_search_btn.clicked.connect(lambda: self.open_currency_search(self.bill_currency_combo))
        curr_layout.addWidget(curr_search_btn)
        add_bill_layout.addLayout(curr_layout, 2, 1)
        
        # Category
        self.bill_category_combo = QComboBox()
        self.update_category_combos()
        add_bill_layout.addWidget(QLabel(STRINGS["category_label"] + ":"), 3, 0)
        
        cat_row = QHBoxLayout()
        cat_row.addWidget(self.bill_category_combo)
        manage_cat_btn = QPushButton("⚙️")
        manage_cat_btn.setFixedWidth(40)
        manage_cat_btn.clicked.connect(self.manage_categories)
        cat_row.addWidget(manage_cat_btn)
        add_bill_layout.addLayout(cat_row, 3, 1)
        
        # Repeat
        self.bill_repeat_combo = QComboBox()
        self.bill_repeat_combo.addItems(FREQUENCIES)
        add_bill_layout.addWidget(QLabel(STRINGS["repeat_label"] + ":"), 4, 0)
        add_bill_layout.addWidget(self.bill_repeat_combo, 4, 1)
        
        # Date
        self.bill_date_input = QDateEdit()
        self.bill_date_input.setCalendarPopup(True)
        self.bill_date_input.setDate(QDate.currentDate())
        add_bill_layout.addWidget(QLabel(STRINGS["due_date_row"] + ":"), 5, 0)
        add_bill_layout.addWidget(self.bill_date_input, 5, 1)
        
        self.bill_is_subscription_chk = QCheckBox(STRINGS["chk_is_subscription"])
        add_bill_layout.addWidget(self.bill_is_subscription_chk, 6, 1)
        
        add_bill_btn = QPushButton(STRINGS["add_bill_button"])
        add_bill_btn.clicked.connect(self.add_bill)
        add_bill_layout.addWidget(add_bill_btn, 7, 0, 1, 2)
        
        add_bill_group.setLayout(add_bill_layout)
        scroll_layout.addWidget(add_bill_group)
        
        # Summary Area (Quick View)
        summary_group = QGroupBox(STRINGS["group_quick_status"])
        summary_layout = QVBoxLayout()
        
        self.total_unpaid_label = QLabel(STRINGS["total_unpaid_label"] + " $0.00")
        self.total_unpaid_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        self.total_unpaid_label.setFont(title_font)
        summary_layout.addWidget(self.total_unpaid_label)
        
        self.remaining_budget_label = QLabel(STRINGS["budget_after_paying_label"] + " $0.00")
        self.remaining_budget_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(self.remaining_budget_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        summary_layout.addWidget(self.progress_bar)
        
        self.rates_status_label = QLabel()
        self.rates_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(self.rates_status_label)

        # Summarize In Currency
        currency_layout = QHBoxLayout()
        currency_layout.addWidget(QLabel(STRINGS["summarize_in_label"]))
        self.summary_currency_combo = LazyCombo(items_provider=self.get_filtered_currency_list, pending_text=None)
        currency_layout.addWidget(self.summary_currency_combo)
        summary_search_btn = QPushButton("🔍 " + STRINGS["sort_name_button"])
        summary_search_btn.clicked.connect(lambda: self.open_currency_search(self.summary_currency_combo))
        currency_layout.addWidget(summary_search_btn)
        currency_layout.addStretch()
        summary_layout.addLayout(currency_layout)
        
        summary_group.setLayout(summary_layout)
        scroll_layout.addWidget(summary_group)
        
        # Support & Data (v5.0)
        about_group = QGroupBox(STRINGS["group_support_data"])
        about_layout = QVBoxLayout()
        
        # Created By
        accent = self.theme_manager.accent_color
        credits = QLabel(f'<a href="https://guns.lol/grouvya" style="color: {accent}; font-weight: bold; text-decoration: none;">{STRINGS["credits_link"]}</a>')
        credits.setAlignment(Qt.AlignmentFlag.AlignCenter)
        credits.setOpenExternalLinks(True)
        font = QFont()
        font.setPointSize(11)
        credits.setFont(font)
        about_layout.addWidget(credits)
        
        about_group.setLayout(about_layout)
        scroll_layout.addWidget(about_group)
        
        # Buttons Row
        btn_layout = QHBoxLayout()
        
        export_btn = QPushButton(STRINGS["btn_export_csv"])
        export_btn.clicked.connect(self.export_csv)
        btn_layout.addWidget(export_btn)
        
        pdf_btn = QPushButton(STRINGS["btn_export_pdf"])
        pdf_btn.clicked.connect(self.export_pdf)
        btn_layout.addWidget(pdf_btn)
        
        about_layout.addLayout(btn_layout)
        about_group.setLayout(about_layout)
        scroll_layout.addWidget(about_group)
        
        # Other Actions
        actions_group = QGroupBox(STRINGS["actions_group_title"])
        actions_layout = QHBoxLayout()
        
        search_btn = QPushButton(STRINGS["btn_search"])
        search_btn.clicked.connect(self.open_search)
        actions_layout.addWidget(search_btn)
        
        converter_btn = QPushButton(STRINGS["converter_button"])
        converter_btn.clicked.connect(self.open_converter)
        actions_layout.addWidget(converter_btn)
        
        settings_btn = QPushButton(STRINGS["settings_button"])
        settings_btn.clicked.connect(self.open_settings)
        actions_layout.addWidget(settings_btn)
        
        tray_btn = QPushButton(STRINGS["btn_minimize_tray"])
        tray_btn.clicked.connect(self.hide_to_tray)
        actions_layout.addWidget(tray_btn)
        
        refresh_btn = QPushButton(STRINGS["refresh_rates_button"])
        refresh_btn.clicked.connect(self.refresh_rates)
        actions_layout.addWidget(refresh_btn)
        
        actions_group.setLayout(actions_layout)
        scroll_layout.addWidget(actions_group)
        
        # Spacer
        scroll_layout.addStretch()

    def setup_unpaid_tab(self):
        layout = QVBoxLayout()
        self.unpaid_tab.setLayout(layout)
        
        # Summary Header
        self.unpaid_summary_label = QLabel(STRINGS["total_unpaid_label"] + " $0.00")
        self.unpaid_summary_label.setObjectName("summaryLabel")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.unpaid_summary_label.setFont(font)
        self.unpaid_summary_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.unpaid_summary_label)

        # Filter Bar
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel(STRINGS["label_filter_category"]))
        self.category_filter_combo = QComboBox()
        self.category_filter_combo.addItem(STRINGS["item_all_categories"])
        self.category_filter_combo.addItems(CATEGORIES)
        # Optimized: Debounce filter to prevent UI lag
        self.category_filter_combo.currentTextChanged.connect(lambda: self.filter_timer.start(300))
        filter_layout.addWidget(self.category_filter_combo)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Table
        self.unpaid_table = QTableWidget()
        self.unpaid_table.setColumnCount(5)
        self.unpaid_table.setHorizontalHeaderLabels([
            STRINGS["header_name"], 
            STRINGS["header_amount"], 
            STRINGS["header_category"], 
            STRINGS["header_due_date"], 
            STRINGS["header_frequency"]
        ])
        self.unpaid_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.unpaid_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.unpaid_table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.unpaid_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.unpaid_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.unpaid_table.customContextMenuRequested.connect(self.show_unpaid_context_menu)
        self.unpaid_table.itemClicked.connect(lambda item: self.show_bill_details(item, is_paid=False))
        layout.addWidget(self.unpaid_table)

    def setup_paid_tab(self):
        layout = QVBoxLayout()
        self.paid_tab.setLayout(layout)
        
        # Summary Header
        self.paid_summary_label = QLabel(STRINGS["label_total_paid"] + ": $0.00")
        self.paid_summary_label.setObjectName("summaryLabel")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.paid_summary_label.setFont(font)
        self.paid_summary_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.paid_summary_label)
        
        # Table
        self.paid_table = QTableWidget()
        self.paid_table.setColumnCount(5)
        self.paid_table.setHorizontalHeaderLabels([
            STRINGS["header_name"], 
            STRINGS["header_amount"], 
            STRINGS["header_category"], 
            STRINGS["header_paid_date"], 
            STRINGS["header_frequency"]
        ])
        self.paid_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.paid_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.paid_table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.paid_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.paid_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.paid_table.customContextMenuRequested.connect(self.show_paid_context_menu)
        self.paid_table.itemClicked.connect(lambda item: self.show_bill_details(item, is_paid=True))
        layout.addWidget(self.paid_table)
    
    def restore_currency_preferences(self):
        """Restore last used currency selections from saved data."""
        try:
            # Block signals to prevent "on_currency_changed" from triggering saves 
            # while we are still restoring the state. This prevents partial data overwrites.
            self.budget_currency_combo.blockSignals(True)
            self.bill_currency_combo.blockSignals(True)
            self.summary_currency_combo.blockSignals(True)
            
            # CRITICAL FIX: Pass session_pin to decrypt data correctly!
            data = self.data_manager.load_data(self.session_pin)
            budget_curr = data.get('budget_currency')
            bill_curr = data.get('bill_currency')
            summary_curr = data.get('summary_currency')
            
            # Helper to match old format "$ (USD)" or new format "$ - US Dollar" to modern key
            def find_display_key(saved_str):
                if not saved_str: return None
                
                # 1. Exact match
                if saved_str in self.currencies: 
                    return saved_str
                
                # 2. Try to extract code from old format "$ (USD)"
                import re
                match = re.search(r'\((.*?)\)', saved_str)
                if match:
                    code = match.group(1)
                    for key, meta in self.currencies.items():
                        if meta['code'] == code: return key
                        
                # 3. Fallback: Search by Symbol in currencies metadata
                # 4. Fallback: Check if saved_str matches any 'code' directly (e.g. "USD")
                for key, meta in self.currencies.items():
                    # If saved string is exactly the code "USD"
                    if saved_str == meta['code']:
                        return key
                        
                    # If saved string contains the name? "British Pound" in "British Pound Sterling"
                    # Only do this if we are desperate.
                    
                # 5. Fuzzy match for cases like "British Pound" vs "British Pound Sterling"
                # If saved_str is in the KEY (ignoring symbol prefix)
                for key in self.currencies:
                    # key is "£ - British Pound Sterling"
                    # saved_str is "British Pound" or "£ - British Pound"
                    if saved_str in key:
                        return key
                        
                return None

            b_key = find_display_key(budget_curr)
            if b_key: 
                print(f"DEBUG: restore found key '{b_key}' for budget. Setting...", flush=True)
                self.budget_currency_combo.setCurrentText(b_key)
            else:
                 print(f"DEBUG: restore FAILED to match budget '{budget_curr}'", flush=True)
            
            bl_key = find_display_key(bill_curr)
            if bl_key: self.bill_currency_combo.setCurrentText(bl_key)
            
            s_key = find_display_key(summary_curr)
            if s_key: self.summary_currency_combo.setCurrentText(s_key)
            
        except Exception as e:
            print(f"DEBUG: restore exception: {e}", flush=True)
            pass
        finally:
            print("DEBUG: restore returning signals to normal", flush=True)
            self.budget_currency_combo.blockSignals(False)
            self.bill_currency_combo.blockSignals(False)
            self.summary_currency_combo.blockSignals(False)
            # Ensure display is updated with restored values
            self.update_display()
    
    def on_currency_changed(self):
        """Handle currency changes from any combo box."""
        print(f"DEBUG: on_currency_changed triggered from UI. Current Budget Text: '{self.budget_currency_combo.currentText()}'", flush=True)
        self.update_display()
        self.save_data()
    

    
    def load_data(self):
        data = self.data_manager.load_data(self.session_pin)
        self.custom_categories = data.get('custom_categories', [])
        
        if data.get('__tampered__'):
            reply = QMessageBox.critical(self, STRINGS["title_security_alert"], 
                                       STRINGS["msg_data_tampered"],
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.restore_backup()
                return
        
        self.unpaid_bills = data.get('unpaid_bills', [])
        self.paid_bills = data.get('paid_bills', [])
        self.budget = float(data.get('budget', 0.0))
        self.savings_goals = data.get('savings_goals', [])
        
        # Update Tabs
        if hasattr(self, 'calendar_tab'):
           self.calendar_tab.refresh_data()
        if hasattr(self, 'savings_tab'):
           self.savings_tab.refresh_data()
        if hasattr(self, 'subscription_tab'):
           self.subscription_tab.refresh_data()
        if hasattr(self, 'savings_tab'):
            self.savings_tab.refresh_data()
        
        self.setUpdatesEnabled(True)
    
    def restore_backup(self):
        """Attempt to restore from backup folder."""
        backup_dir = os.path.join(self.data_manager.config_dir, 'backups')
        if not os.path.exists(backup_dir):
            QMessageBox.warning(self, STRINGS["title_restore_failed"], STRINGS["msg_no_backups"])
            return

        backups = sorted([f for f in os.listdir(backup_dir) if f.startswith('bill_data_')], reverse=True)
        if not backups:
            QMessageBox.warning(self, STRINGS["title_restore_failed"], STRINGS["msg_no_backups"])
            return
            
        latest = os.path.join(backup_dir, backups[0])
        try:
            # Hardened: Verify integrity BEFORE restoring 🛡️
            with open(latest, 'r', encoding='utf-8') as f:
                test_load = json.load(f)
            if not isinstance(test_load, dict) or 'unpaid_bills' not in test_load:
                raise ValueError("Backup file is corrupt or invalid format")

            # Copy backup to main data file
            import shutil
            shutil.copy2(latest, self.data_manager.data_file)
            QMessageBox.information(self, STRINGS["title_restored"], STRINGS["msg_restored"])
            self.load_data()
            self.update_display()
        except Exception as e:
            logging.exception("Backup restore failed")
            QMessageBox.critical(self, STRINGS["title_error"], f"{STRINGS['msg_restore_error'].format(e)}")
    
    def save_data(self):
        data = {
            'budget': self.budget,
            'unpaid_bills': self.unpaid_bills,
            'paid_bills': self.paid_bills,
            'budget_currency': self.budget_currency_combo.currentText(),
            'bill_currency': self.bill_currency_combo.currentText(),
            'summary_currency': self.summary_currency_combo.currentText(),
            'custom_categories': self.custom_categories
        }
        self.data_manager.save_data(data, self.session_pin)
    
    def set_budget(self):
        try:
            raw_val = self.budget_input.text()
            amount = strict_float(raw_val) # Hardened parsing
            curr = self.budget_currency_combo.currentText()
            
            with self.data_lock:
                rate = self.exchange_rates.get(curr, 1)
                if rate <= 0:
                    raise ValueError
                self.budget = amount / rate
            
            self.save_data()
            QMessageBox.information(self, STRINGS["info_budget_set"], 
                                  STRINGS["info_budget_set_to"].format(f"{self.currencies.get(curr, {}).get('symbol', '') if isinstance(self.currencies.get(curr), dict) else self.currencies.get(curr, '')}{amount:,.2f}"))
            self.update_display()
        except ValueError:
            QMessageBox.warning(self, STRINGS["dialog_input_error"], STRINGS["error_valid_number"])
        except Exception as e:
            logging.exception("Failed to set budget")
            QMessageBox.critical(self, STRINGS["title_error"], f"Failed to set budget: {e}")
    
    def add_bill(self):
        name = sanitize_input(self.bill_name_input.text()) # Hardened: Strip hidden chars
        amount_text = self.bill_amount_input.text()
        currency = self.bill_currency_combo.currentText()
        category = self.bill_category_combo.currentText()
        repeat = self.bill_repeat_combo.currentText()
        due_date = self.bill_date_input.date().toString('yyyy-MM-dd')
        
        if not name or not amount_text:
            QMessageBox.warning(self, STRINGS["dialog_input_error"], STRINGS["error_enter_name_amount"])
            return
            
        try:
            amount = strict_float(amount_text) # Hardened: Locale-aware parsing
            if amount <= 0:
                raise ValueError
            if amount > 1000000000:
                QMessageBox.warning(self, STRINGS["dialog_input_error"], STRINGS["msg_amount_large"])
                return
        except ValueError:
            QMessageBox.warning(self, STRINGS["dialog_input_error"], STRINGS["error_positive_amount"])
            return
        except Exception as e:
            logging.warning(f"Invalid bill amount format: {e}")
            QMessageBox.warning(self, STRINGS["dialog_input_error"], STRINGS["msg_invalid_format"])
            return
        
        bill = {
            'name': name, 
            'amount': amount, 
            'currency': currency, 
            'category': get_canonical_category(category),
            'repeat_freq': get_canonical_frequency(repeat),
            'due_date': due_date,
            'is_subscription': self.bill_is_subscription_chk.isChecked(),
            'created_at': datetime.now().isoformat()
        }
        self.unpaid_bills.append(bill)
        
        # Reset inputs
        self.bill_name_input.clear()
        self.bill_amount_input.clear()
        
        self.save_data()
        self.update_display()
        
        QMessageBox.information(self, STRINGS["title_success"], STRINGS["msg_bill_added"].format(name))

    def pay_bill(self, bill, silent=False):
        """Pay a bill and move to paid list. Handle recurrence."""
        if not silent:
            reply = QMessageBox.question(self, STRINGS["dialog_confirm_payment"],
                                       STRINGS["confirm_payment_msg"].format(bill['name']),
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply != QMessageBox.StandardButton.Yes:
                return
            rate = self.exchange_rates.get(bill['currency'], 1)
            # Find closest rate or default
            
            # Handle Recurrence
            # Use canonical frequency for logic (always English)
            freq = get_canonical_frequency(bill.get('repeat_freq', 'No Repeat'))
            
            if freq != 'No Repeat':
                try:
                    # Use QDate for robust date math
                    qd = QDate.fromString(bill['due_date'], 'yyyy-MM-dd')
                    if not qd.isValid():
                        qd = QDate.currentDate()
                    
                    if freq == 'Weekly': qd = qd.addDays(7)
                    elif freq == 'Monthly': qd = qd.addMonths(1)
                    elif freq == 'Yearly': qd = qd.addYears(1)
                    
                    new_bill = bill.copy()  # Use copy to create new recurring bill
                    new_bill['due_date'] = qd.toString('yyyy-MM-dd')
                    new_bill['created_at'] = datetime.now().isoformat()
                    
                    # Auto-create next bill
                    self.unpaid_bills.append(new_bill)
                    
                    # Notify user
                    self.tray_icon.showMessage(STRINGS["title_recurring_created"], 
                                             STRINGS["msg_recurring_created"].format(bill['name'], new_bill['due_date']),
                                             QSystemTrayIcon.MessageIcon.Information, 3000)
                except Exception as e:
                    logging.error(f"Recurrence error: {e}")

            if bill in self.unpaid_bills:
                self.unpaid_bills.remove(bill)
            self.paid_bills.insert(0, bill) # Add to top
            self.save_data()
            self.update_display()

    def open_contact(self):
        webbrowser.open("https://guns.lol/grouvya")

    def open_donate(self):
        webbrowser.open("https://revolut.me/grouvya")

    def export_csv(self):
        """Export data to CSV."""
        file_path, _ = QFileDialog.getSaveFileName(self, STRINGS["title_export_data"], "bill_history.csv", STRINGS["filter_csv"])
        if not file_path:
            return
            
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "Amount", "Currency", "Category", "Due Date", "Frequency", "Status"])
                
                for b in self.unpaid_bills:
                    writer.writerow([b['name'], b['amount'], b['currency'], b.get('category',''), b['due_date'], b.get('repeat_freq',''), "Unpaid"])
                    
                for b in self.paid_bills:
                    writer.writerow([b['name'], b['amount'], b['currency'], b.get('category',''), b['due_date'], b.get('repeat_freq',''), "Paid"])
            
            QMessageBox.information(self, STRINGS["title_export_success"], STRINGS["msg_export_success"].format(file_path))
        except Exception as e:
            QMessageBox.critical(self, STRINGS["title_export_failed"], str(e))

    def export_pdf(self):
        """Export a PDF report utilizing the new generator."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"BillTracker_Report_{timestamp}.pdf"
        file_path, _ = QFileDialog.getSaveFileName(self, STRINGS.get("title_save_report", "Save Report"), filename, "PDF Files (*.pdf)")
        
        if not file_path:
            return

        # Prepare Data
        # 1. Capture Charts
        chart_images = []
        import tempfile
        temp_dir = tempfile.gettempdir()
        
        try:
            # Budget Chart
            p1 = os.path.join(temp_dir, f"budget_{timestamp}.png")
            self.budget_chart.grab().save(p1)
            chart_images.append(p1)
            
            # Category Chart
            p2 = os.path.join(temp_dir, f"category_{timestamp}.png")
            self.category_chart.grab().save(p2)
            chart_images.append(p2)
            
            # Trends Chart
            p3 = os.path.join(temp_dir, f"trends_{timestamp}.png")
            self.trends_chart.grab().save(p3)
            chart_images.append(p3)
        except Exception as e:
            logging.warning(f"Failed to capture charts: {e}")

        # 2. Summary Data
        # Recalculate summary totals
        with self.data_lock:
             rates = self.exchange_rates.copy()
             
        curr = self.summary_currency_combo.currentText()
        summary_rate = rates.get(curr, 1)
        
        total_unpaid = sum(b['amount'] / (rates.get(b['currency'], 1.0) or 1.0) for b in self.unpaid_bills)
        
        # Calculate monthly paid (simple filter for current month)
        now = datetime.now()
        current_month_paid = 0
        for b in self.paid_bills:
            try:
                pd_str = b.get('paid_date', '')
                if pd_str:
                    pd = datetime.strptime(pd_str, "%Y-%m-%d")
                    if pd.year == now.year and pd.month == now.month:
                        current_month_paid += b['amount'] / (rates.get(b['currency'], 1.0) or 1.0)
            except:
                pass

        # Recalculate strictly
        summary = {
            'total_unpaid': total_unpaid * summary_rate,
            'total_paid': current_month_paid * summary_rate,
            'budget': self.budget * summary_rate,
            'remaining': (self.budget - total_unpaid) * summary_rate,
            'currency': self.currencies.get(curr, {}).get('symbol', '$') if isinstance(self.currencies.get(curr), dict) else self.currencies.get(curr, '$')
        }

        # 3. Generate
        generator = PDFReportGenerator(file_path)
        success = generator.generate(summary, self.unpaid_bills, chart_images)
        
        # Cleanup
        for p in chart_images:
            if os.path.exists(p):
                try:
                    os.remove(p)
                except: pass
                
        if success:
            QMessageBox.information(self, STRINGS["title_success"], STRINGS["msg_report_generated"])
        else:
            QMessageBox.critical(self, STRINGS["title_error"], STRINGS["msg_report_failed"])

    def check_due_bills(self):
        """Check for bills due today or tomorrow."""
        today = date.today()
        due_bills = []
        count = 0
        
        # Load preference once outside the loop
        config = self.data_manager.load_config(self.session_pin)
        days_advance = config.get('reminder_days', 1)
        
        for bill in self.unpaid_bills:
            try:
                due = datetime.strptime(bill['due_date'], '%Y-%m-%d').date()
                delta = (due - today).days
                
                if delta <= days_advance:
                    due_bills.append(bill)
                    count += 1
            except: pass
            
        if count > 0:
            # Actionable Notification (v6.6.0)
            self.toast = ToastNotification(self, due_bills, self.theme_manager)
            self.toast.show()
            
            # Tray Fallback (Legacy)
            self.tray_icon.showMessage(
                STRINGS["notification_title"],
                STRINGS["notification_msg"].format(count),
                QSystemTrayIcon.MessageIcon.Information,
                3000
            )
            
            # Webhook Notification (Daily check)
            if config.get('webhooks_enabled', False) and config.get('webhook_url'):
                current_time = datetime.now().strftime('%H:%M')
                target_time = config.get('reminder_time', '09:00')
                
                # Cooldown check: Only once today
                today_str = date.today().strftime('%Y-%m-%d')
                last_sent = config.get('last_webhook_sent', '')
                
                if current_time >= target_time and last_sent != today_str:
                    self.send_webhook_notification(count)
                    config['last_webhook_sent'] = today_str
                    self.data_manager.save_config(config, self.session_pin)

    def send_webhook_notification(self, count):
        config = self.data_manager.load_config(self.session_pin)
        url = config.get('webhook_url')
        if not url: return
        
        try:
            import json
            import urllib.request
            msg = STRINGS["notification_msg"].format(count)
            data = json.dumps({"content": f"📅 **BillTracker**: {msg}"}).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response: pass
        except Exception as e:
            print(f"Webhook delivery failed: {e}")

    def get_budget_remaining(self):
        """Helper for Mini Mode to calculate remaining budget using in-memory data (v6.3.3)."""
        try:
            with self.data_lock:
                current_budget = self.budget
                rates = self.exchange_rates.copy()
                unpaid = list(self.unpaid_bills)
            
            if current_budget <= 0:
                return "--"
            
            # Get summary currency settings
            summary_curr = self.summary_currency_combo.currentText()
            # Extract code if needed "$ (USD)" -> "USD"
            import re
            curr_match = re.search(r'\((.*?)\)', summary_curr)
            if curr_match:
                summary_curr = curr_match.group(1)
            
            metadata = self.currencies.get(summary_curr, {'symbol': '$'})
            summary_symbol = metadata.get('symbol', '$') if isinstance(metadata, dict) else metadata
            summary_rate = rates.get(summary_curr, 1.0)
            
            if summary_rate <= 0:
                summary_rate = 1.0

            # Calculate total unpaid in USD
            total_unpaid_usd = sum(b['amount'] / (rates.get(b['currency'], 1.0) or 1.0) 
                                  for b in unpaid)
            
            remaining_usd = current_budget - total_unpaid_usd
            remaining_converted = remaining_usd * summary_rate
            
            return f"{summary_symbol}{remaining_converted:,.2f}"
        except Exception as e:
            logging.debug(f"Mini Mode Budget Error: {e}")
            return "--"

    def switch_to_mini_mode(self):
        self.mini_mode = MiniTrackerWidget(self, STRINGS, self.theme_manager)
        self.mini_mode.show()
        self.hide()
    
    def refresh_rates(self):
        self.api_thread = APIThread()
        self.api_thread.finished.connect(self.handle_api_result)
        self.api_thread.start()
    
    def handle_api_result(self, result):
        if result['status'] == 'success':
            data = result['data']
            api_rates = data.get('conversion_rates', {})
            updated_rates = {}
            for curr_display in self.currencies:
                meta = self.currencies.get(curr_display)
                code = meta['code']
                if code in api_rates:
                    updated_rates[curr_display] = api_rates[code]
            
            # Ensure USD base exists
            for k, v in self.currencies.items():
                if v['code'] == 'USD':
                    updated_rates[k] = 1.0
            
            with self.data_lock: # Thread Safety: Update shared state
                self.exchange_rates = updated_rates
                
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.rates_status_label.setText(STRINGS["rates_updated_at"].format(now))
            self.data_manager.save_rates_cache(data)
        else:
            self.rates_status_label.setText(result.get('message', STRINGS["api_error"]))
        self.update_display()
    
    def setup_chart_tab(self):
        layout = QVBoxLayout()
        self.chart_tab.setLayout(layout)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        widget = QWidget()
        layout.addWidget(scroll)
        scroll.setWidget(widget)
        
        vbox = QVBoxLayout()
        widget.setLayout(vbox)
        
        # Budget Chart
        vbox.addWidget(QLabel(STRINGS["chart_budget_title"]))
        self.budget_chart = ChartWidget()
        vbox.addWidget(self.budget_chart)
        
        # Category Chart
        vbox.addWidget(QLabel(STRINGS["chart_category_title"]))
        self.category_chart = ChartWidget()
        vbox.addWidget(self.category_chart)
        
        # Trends Chart
        vbox.addWidget(QLabel(STRINGS["label_monthly_history"]))
        self.trends_chart = TrendsWidget()
        vbox.addWidget(self.trends_chart)
        
        # Export PDF Button
        export_pdf_btn = QPushButton(STRINGS.get("btn_export_pdf", "📄 Export PDF Report"))
        export_pdf_btn.clicked.connect(self.export_pdf)
        vbox.addWidget(export_pdf_btn)


    def setup_about_tab(self):
        """Setup About tab with lazy-loaded README content."""
        layout = QVBoxLayout()
        self.about_tab.setLayout(layout)
        
        # Create scrollable text area
        self.about_scroll = QScrollArea()
        self.about_scroll.setWidgetResizable(True)
        self.about_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.about_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Text widget for README
        self.about_text_widget = QLabel()
        self.about_text_widget.setWordWrap(True)
        self.about_text_widget.setTextFormat(Qt.TextFormat.MarkdownText)
        self.about_text_widget.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.about_text_widget.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.about_text_widget.setStyleSheet("padding: 20px; font-size: 11pt;")
        self.about_text_widget.setText("Loading...")
        
        self.about_scroll.setWidget(self.about_text_widget)
        layout.addWidget(self.about_scroll)
        
        # Buttons Row
        btn_row = QHBoxLayout()
        
        self.contact_btn = QPushButton(STRINGS["btn_contact"])
        self.contact_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.contact_btn.setStyleSheet("""
            QPushButton {
                background-color: #8338ec; 
                color: white; 
                font-weight: bold;
                padding: 10px;
                font-size: 11pt;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #9d4edd;
            }
        """)
        self.contact_btn.clicked.connect(self.open_contact)
        btn_row.addWidget(self.contact_btn)
        
        self.donate_btn = QPushButton(STRINGS["btn_donate"])
        self.donate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.donate_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff006e; 
                color: white; 
                font-weight: bold;
                padding: 10px;
                font-size: 11pt;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ff5c8d;
            }
        """)
        self.donate_btn.clicked.connect(self.open_donate)
        btn_row.addWidget(self.donate_btn)
        
        layout.addLayout(btn_row)


    def _on_tab_changed(self, index):
        """Handle tab changes for lazy loading content."""
        # 3: Trends, 4: Calendar, 5: Subscriptions, 6: About
        if index == 3:
            # Refresh Trends
            self.update_charts()
        elif index == 4:
            # Refresh Calendar
            if hasattr(self, 'calendar_tab'):
                self.calendar_tab.refresh_data()
        elif index == 5:
            # Refresh Subscriptions
            if hasattr(self, 'subscription_tab'):
                self.subscription_tab.refresh_data()
        elif index == 6:
            # Refresh Savings
            if hasattr(self, 'savings_tab'):
                self.savings_tab.refresh_data()
        elif index == 7:
            # Refresh About
            self._load_readme()

    def update_category_combos(self):
        """Update all category dropdowns with default + custom categories."""
        full_list = get_full_categories(self.custom_categories)
        self.bill_category_combo.clear()
        self.bill_category_combo.addItems(full_list)
        if hasattr(self, 'category_filter_combo'):
            self.category_filter_combo.clear()
            self.category_filter_combo.addItem(STRINGS["item_all_categories"])
            self.category_filter_combo.addItems(full_list)

    def manage_categories(self):
        """Open the category management dialog."""
        dialog = CategoryManagerDialog(self, self.custom_categories.copy())
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.custom_categories = dialog.get_data()
            self.save_data()
            self.update_category_combos()
            self.update_display()


    def _load_readme(self):
        """Lazy load README content when About tab is opened (supports English and Georgian)."""
        if self.about_loaded:
            return
            
        # Select README based on language
        # We check if the app title in the current STRINGS matches the Georgian one
        is_georgian = STRINGS.get("app_title") == TRANSLATIONS["Georgian"].get("app_title")
        readme_filename = 'README_GE.md' if is_georgian else 'README.md'
            
        readme_path = resource_path(readme_filename)
        try:
            if os.path.exists(readme_path):
                with open(readme_path, 'r', encoding='utf-8') as f:
                    readme_content = f.read()
            else:
                # Fallback to English if Georgian file is missing
                readme_path = resource_path('README.md')
                with open(readme_path, 'r', encoding='utf-8') as f:
                    readme_content = f.read()
                    
            self.about_text_widget.setText(readme_content)
            
            # Explicitly trigger layout update many things happen after loading markdown
            # to ensure scrollbars are correctly sized.
            self.about_text_widget.adjustSize()
            if hasattr(self, 'about_scroll'):
                self.about_scroll.update()

        except Exception as e:
            self.about_text_widget.setText(f"# Error loading documentation\n\n{str(e)}")
            logging.error(f"Failed to load README ({readme_filename}): {e}")
        
        self.about_loaded = True


    def handle_calendar_click(self, date):
        dt = date.toString("yyyy-MM-dd")
        with self.data_lock:
            rates = self.exchange_rates.copy()
            summary_curr = self.summary_currency_combo.currentText()
            metadata = self.currencies.get(summary_curr, {'symbol': '$'})
            summary_symbol = metadata.get('symbol', '$') if isinstance(metadata, dict) else summary_symbol
            summary_rate = rates.get(summary_curr, 1)

        bills_on_day = [b for b in self.unpaid_bills if b.get('due_date') == dt]
        if bills_on_day:
            info_lines = []
            for b in bills_on_day:
                b_rate = rates.get(b['currency'], 1.0) or 1.0
                amt_converted = (b['amount'] / b_rate) * summary_rate
                info_lines.append(f"• {b['name']}: {summary_symbol}{amt_converted:,.2f}")
            
            self.calendar_label.setText(f"<b>Bills due on {dt}:</b><br/>" + "<br/>".join(info_lines))
            self.calendar_label.setStyleSheet("color: #ff4d4d; font-size: 11pt;")
        else:
            self.calendar_label.setText(STRINGS["label_no_bills_due"].format(dt))
            self.calendar_label.setStyleSheet("color: #888; font-size: 10pt;")

    def handle_calendar_double_click(self, date):
        """Pre-fill Add Bill with the double-clicked date."""
        self.tabs.setCurrentIndex(0) # Switch to Dashboard
        self.bill_date_input.setDate(date)
        self.bill_name_input.setFocus()
        
    def update_charts(self):
        if not hasattr(self, 'budget_chart'):
            return
            
        with self.data_lock: # Hardened: Read state snapshot for consistent chart rendering
            rates = self.exchange_rates.copy()
            current_budget = self.budget
            
        # 1. Budget vs Expenses
        total_unpaid = 0.0
        budget_curr = self.budget_currency_combo.currentText()
        target_rate = rates.get(budget_curr, 1) or 1
        
        for bill in self.unpaid_bills:
            b_rate = rates.get(bill['currency'], 1.0) or 1.0 # Hardened Fallback
            total_unpaid += (bill['amount'] / b_rate) * target_rate
            
        self.budget_chart.set_data({STRINGS["label_remaining"]: max(0, current_budget), STRINGS["label_unpaid_bills_chart"]: total_unpaid})
        
        # 2. Expenses by Category (Unpaid)
        cat_data = {}
        for bill in self.unpaid_bills:
            cat_canonical = bill.get('category', 'Other')
            cat_display = get_display_category(cat_canonical)
            b_rate = rates.get(bill['currency'], 1.0) or 1.0 # Hardened Fallback
            amt = (bill['amount'] / b_rate) * target_rate
            cat_data[cat_display] = cat_data.get(cat_display, 0) + amt
            
        self.category_chart.set_data(cat_data)
        
        # 3. Trends (Paid History by Month)
        trends_data = {}
        for bill in self.paid_bills:
            d = bill.get('due_date', '')
            if len(d) >= 7:
                key = d[:7] # YYYY-MM
                b_rate = rates.get(bill['currency'], 1.0) or 1.0 # Hardened Fallback
                amt = (bill['amount'] / b_rate) * target_rate
                trends_data[key] = trends_data.get(key, 0) + amt
        
        if hasattr(self, 'trends_chart'):
            self.trends_chart.set_data(trends_data)
        
        # Update Calendar
        if hasattr(self, 'calendar_tab'):
            self.calendar_tab.refresh_data()






    def update_display(self):
        self.update_charts()
        
        with self.data_lock: # Hardened: Consistent data read
            rates = self.exchange_rates.copy()
            current_budget = self.budget
            
        # Update budget display
        curr = self.budget_currency_combo.currentText()
        rate = rates.get(curr, 1)
        if rate > 0:
            self.budget_input.setText(f"{current_budget * rate:,.2f}")
        
        # Update summary
        summary_curr = self.summary_currency_combo.currentText()
        meta = self.currencies.get(summary_curr, {'symbol': '$'})
        summary_symbol = meta.get('symbol', '$')
        summary_rate = rates.get(summary_curr, 1)
        
        if summary_rate > 0:
            total_unpaid_usd = 0
            for b in self.unpaid_bills:
                b_rate = self.get_exchange_rate(b.get('currency', 'USD'))
                total_unpaid_usd += b['amount'] / (b_rate or 1.0)

            remaining_usd = current_budget - total_unpaid_usd
            
            self.total_unpaid_label.setText(f"{STRINGS['total_unpaid_label']} {summary_symbol}{total_unpaid_usd * summary_rate:,.2f}")
            self.remaining_budget_label.setText(f"{STRINGS['budget_after_paying_label']} {summary_symbol}{remaining_usd * summary_rate:,.2f}")
            
            if current_budget > 0:
                percentage = remaining_usd / current_budget
                self.progress_bar.setValue(max(0, int(percentage * 100)))
                p_colors = self.theme_manager.get_palette()
                if percentage < 0.25:
                    self.progress_bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {p_colors['danger']}; }}")
                elif percentage < 0.50:
                    self.progress_bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {p_colors['warning']}; }}")
                else:
                    self.progress_bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {p_colors['success']}; }}")
            
            # Update Dashboard Savings Progress (v6.7.0)
            if hasattr(self, 'dash_savings_progress'):
                total_sav_usd = 0.0
                total_tar_usd = 0.0
                for g in self.savings_goals:
                    g_rate = self.get_exchange_rate(g.get('currency', 'USD'))
                    total_sav_usd += float(g['current']) / (g_rate or 1.0)
                    total_tar_usd += float(g['target']) / (g_rate or 1.0)
                
                if total_tar_usd > 0:
                    percent = min(100, int((total_sav_usd / total_tar_usd) * 100))
                    self.dash_savings_progress.setValue(percent)
                    mid_symbol = self.currencies.get(summary_curr, {'symbol': '$'}).get('symbol', '$')
                    self.dash_savings_stats.setText(f"{mid_symbol}{total_sav_usd * summary_rate:,.2f} / {mid_symbol}{total_tar_usd * summary_rate:,.2f}")
                else:
                    self.dash_savings_progress.setValue(0)
                    self.dash_savings_stats.setText("0.00 / 0.00")
        
        
        # Calculate and Update Unpaid Bills Summary
        self.unpaid_summary_label.setText(f"{STRINGS['total_unpaid_label']}: {summary_symbol}{total_unpaid_usd * summary_rate:,.2f}")
        
        # Calculate Total Paid
        total_paid_usd = 0
        for b in self.paid_bills:
            b_rate = self.get_exchange_rate(b.get('currency', 'USD'))
            total_paid_usd += b['amount'] / (b_rate or 1.0)
            
        self.paid_summary_label.setText(f"{STRINGS['label_total_paid']}: {summary_symbol}{total_paid_usd * summary_rate:,.2f}")
        
        # Update Tables
        self.update_unpaid_table_view()
        self.update_paid_table_view()
        
        # v6.3.1: Ensure Subscription Tab stays in sync
        if hasattr(self, 'subscription_tab'):
            self.subscription_tab.refresh_data()

    def update_unpaid_table_view(self):
        """Update only the unpaid bills table (optimized)."""
        self.unpaid_table.setRowCount(0)
        
        # Filter Logic
        filter_cat = getattr(self, 'category_filter_combo', None)
        target_cat = filter_cat.currentText() if filter_cat else STRINGS["item_all_categories"]
        target_canonical = get_canonical_category(target_cat)
        
        filtered_bills = []
        for bill in self.unpaid_bills:
            if target_cat == STRINGS["item_all_categories"] or bill.get('category') == target_canonical:
                filtered_bills.append(bill)
        
        self.unpaid_table.setRowCount(len(filtered_bills))
        
        for i, bill in enumerate(filtered_bills):
            metadata = self.currencies.get(bill['currency'], {'symbol': '$'})
            symbol = metadata.get('symbol', '$') if isinstance(metadata, dict) else metadata
            
            # Name
            name_item = QTableWidgetItem(bill['name'])
            name_item.setData(Qt.ItemDataRole.UserRole, bill)
            # Amount
            amount_item = QTableWidgetItem(f"{symbol}{bill['amount']:,.2f}")
            # Category
            cat_display = get_display_category(bill.get('category', 'Other'))
            cat_item = QTableWidgetItem(cat_display)
            # Due Date
            due_date = bill.get('due_date', STRINGS["no_date_label"])
            date_item = QTableWidgetItem(due_date)
            # Frequency
            freq_display = get_display_frequency(bill.get('repeat_freq', 'No Repeat'))
            freq_item = QTableWidgetItem(freq_display)
            
            # Check overdue
            try:
                due_raw = bill.get('due_date', '')
                if safe_parse_date(due_raw, None):
                    due_dt = datetime.strptime(due_raw, '%Y-%m-%d').date()
                    if due_dt < date.today():
                        for item in [name_item, amount_item, cat_item, date_item, freq_item]:
                            item.setForeground(QColor('#ff4d4d')) # Red text
            except Exception as e:
                logging.error(f"Error checking overdue status for {bill.get('name')}: {e}")
                
            self.unpaid_table.setItem(i, 0, name_item)
            self.unpaid_table.setItem(i, 1, amount_item)
            self.unpaid_table.setItem(i, 2, cat_item)
            self.unpaid_table.setItem(i, 3, date_item)
            self.unpaid_table.setItem(i, 4, freq_item)

    def update_paid_table_view(self):
        """Update the paid bills history table."""
        self.paid_table.setRowCount(0)
        self.paid_table.setRowCount(len(self.paid_bills))
        
        for i, bill in enumerate(self.paid_bills):
            metadata = self.currencies.get(bill['currency'], {'symbol': '$'})
            symbol = metadata.get('symbol', '$') if isinstance(metadata, dict) else metadata
            
            name_item = QTableWidgetItem(bill['name'])
            name_item.setData(Qt.ItemDataRole.UserRole, bill)
            self.paid_table.setItem(i, 0, name_item)
            self.paid_table.setItem(i, 1, QTableWidgetItem(f"{symbol}{bill['amount']:,.2f}"))
            self.paid_table.setItem(i, 2, QTableWidgetItem(bill.get('category', 'Other')))
            self.paid_table.setItem(i, 3, QTableWidgetItem(bill.get('due_date', '-')))
            self.paid_table.setItem(i, 4, QTableWidgetItem(bill.get('repeat_freq', '-')))

    def show_unpaid_context_menu(self, position):
        """Show context menu for unpaid bills table."""
        selected_items = self.unpaid_table.selectedItems()
        selected_rows = sorted(list(set(item.row() for item in selected_items)), reverse=True)
        
        if not selected_rows:
            return
            
        # Get bills for all selected rows
        bills_to_process = []
        for row_idx in selected_rows:
            item = self.unpaid_table.item(row_idx, 0)
            if item:
                bill_data = item.data(Qt.ItemDataRole.UserRole)
                if bill_data:
                    bills_to_process.append(bill_data)

        if not bills_to_process:
            return

        menu = QMenu()
        
        # Adjust labels if multiple selected
        is_multiple = len(bills_to_process) > 1
        pay_label = STRINGS["menu_pay_bill"] if not is_multiple else f"{STRINGS['menu_pay_bill']} ({len(bills_to_process)})"
        delete_label = STRINGS["menu_delete_bill"] if not is_multiple else f"{STRINGS['menu_delete_bill']} ({len(bills_to_process)})"
        
        pay_action = menu.addAction(pay_label)
        # Edit only allowed for single selection
        edit_action = menu.addAction(STRINGS["menu_edit_bill"]) if not is_multiple else None
        delete_action = menu.addAction(delete_label)
        
        action = menu.exec(self.unpaid_table.viewport().mapToGlobal(position))
        
        if action == pay_action:
            if is_multiple:
                confirm = QMessageBox.question(self, STRINGS["dialog_confirm_payment"],
                                            f"Pay {len(bills_to_process)} selected bills?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if confirm == QMessageBox.StandardButton.Yes:
                    for b in bills_to_process:
                        self.pay_bill(b, silent=True)
                    self.save_data()
                    self.update_display()
            else:
                self.pay_bill(bills_to_process[0])
        elif edit_action and action == edit_action:
            self.edit_bill(bills_to_process[0])
        elif action == delete_action:
            if is_multiple:
                confirm = QMessageBox.question(self, STRINGS["dialog_confirm_delete"],
                                            f"Delete {len(bills_to_process)} selected bills?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if confirm == QMessageBox.StandardButton.Yes:
                    for b in bills_to_process:
                        if b in self.unpaid_bills:
                            self.unpaid_bills.remove(b)
                    self.save_data()
                    self.update_display()
            else:
                self.delete_bill(bills_to_process[0])

    def show_paid_context_menu(self, position):
        """Show context menu for paid bills table."""
        selected_items = self.paid_table.selectedItems()
        selected_rows = sorted(list(set(item.row() for item in selected_items)), reverse=True)
        
        if not selected_rows:
            return
            
        bills_to_process = []
        for row_idx in selected_rows:
            item = self.paid_table.item(row_idx, 0)
            if item:
                bill_data = item.data(Qt.ItemDataRole.UserRole)
                if bill_data:
                    bills_to_process.append((row_idx, bill_data))

        if not bills_to_process:
            return

        is_multiple = len(bills_to_process) > 1
        restore_label = STRINGS["menu_restore_unpaid"] if not is_multiple else f"{STRINGS['menu_restore_unpaid']} ({len(bills_to_process)})"
        delete_label = STRINGS["menu_delete_permanently"] if not is_multiple else f"{STRINGS['menu_delete_permanently']} ({len(bills_to_process)})"

        menu = QMenu()
        restore_action = menu.addAction(restore_label)
        delete_action = menu.addAction(delete_label)
        
        action = menu.exec(self.paid_table.viewport().mapToGlobal(position))
        
        if action == restore_action:
            for row_idx, bill in bills_to_process:
                # Need to find the actual index in paid_bills because table might be filtered or sorted differently?
                # Actually paid_table usually matches paid_bills 1:1 currently.
                if bill in self.paid_bills:
                    self.paid_bills.remove(bill)
                    self.unpaid_bills.append(bill)
            self.save_data()
            self.update_display()
        elif action == delete_action:
            msg = STRINGS["msg_confirm_delete_history"].format(bills_to_process[0][1]['name']) if not is_multiple else f"Delete {len(bills_to_process)} bills from history?"
            reply = QMessageBox.question(self, STRINGS["title_confirm_delete_history"], 
                                       msg,
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                for row_idx, bill in bills_to_process:
                    if bill in self.paid_bills:
                        self.paid_bills.remove(bill)
                self.save_data()
                self.update_display()

    def unpaid_list_item_clicked(self, item):
        """Handle clicks on unpaid list items (load more)."""
        if not item:
            return
        data = item.data(Qt.ItemDataRole.UserRole)
        if data == '__load_more__':
            self._unpaid_page = getattr(self, '_unpaid_page', 1) + 1
            self.update_display()

    def paid_list_item_clicked(self, item):
        if not item:
            return
        data = item.data(Qt.ItemDataRole.UserRole)
        if data == '__load_more_paid__':
            self._paid_page = getattr(self, '_paid_page', 1) + 1
            self.update_display()
    

    
    def edit_bill(self, bill):
        """Edit an existing bill."""
        dialog = BillEditorDialog(self, bill, self.currencies)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_data = dialog.get_data()
            if updated_data:
                # Find and update the bill
                for i, b in enumerate(self.unpaid_bills):
                    if b == bill:
                        self.unpaid_bills[i] = updated_data
                        self.save_data()
                        self.update_display()
                        break
    
    def delete_bill(self, bill):
        """Delete a bill with confirmation."""
        reply = QMessageBox.question(self, STRINGS["dialog_confirm_delete"],
                                   STRINGS["confirm_delete_msg"].format(bill['name']),
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if bill in self.unpaid_bills:
                self.unpaid_bills.remove(bill)
            elif bill in self.paid_bills:
                self.paid_bills.remove(bill)
            self.save_data()
            self.update_display()
    
    def sort_by_name(self):
        self.unpaid_bills.sort(key=lambda b: b['name'].lower())
        self.update_display()
    
    def sort_by_date(self):
        self.unpaid_bills.sort(key=lambda b: safe_parse_date(b.get('due_date')))
        self.update_display()
    
    def sort_by_amount(self):
        with self.data_lock:
            rates = self.exchange_rates.copy()
        self.unpaid_bills.sort(key=lambda b: b['amount'] / (rates.get(b['currency'], 1.0) or 1.0), reverse=True)
        self.update_display()
    
    def open_converter(self):
        dialog = ConverterWindow(self, self.currencies, self.exchange_rates)
        dialog.exec()

    def import_bank_statement(self):
        """Open CSV import dialog and process results."""
        dialog = CSVImportDialog(self, self.currencies)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_bills = dialog.get_imported_bills()
            if new_bills:
                self.unpaid_bills.extend(new_bills)
                self.save_data()
                self.update_display()
                QMessageBox.information(
                    self, 
                    STRINGS["title_csv_import"], 
                    STRINGS["msg_csv_mapped"].format(len(new_bills))
                )
    
    def open_settings(self):
        try:
            dialog = SettingsDialog(self, self.data_manager)
            if dialog.exec():
                # Reload settings that affect live behavior
                config = self.data_manager.load_config(self.session_pin)
                self.auto_lock_enabled = config.get('auto_lock_enabled', False)
                self.idle_timeout_minutes = config.get('idle_timeout_minutes', 5)
                self.lock_on_minimize = config.get('lock_on_minimize', False)
                self.minimize_to_tray = config.get('minimize_to_tray', False)
                
                # Restart auto-lock timer with new settings
                self.check_idle_timeout()
        except Exception as e:
             logging.exception("Critical error opening settings")
             QMessageBox.critical(self, STRINGS["title_error"], f"Error opening settings: {e}")
    
    def clear_data(self):
        reply = QMessageBox.question(self, STRINGS["dialog_clear_data"],
                                   STRINGS["confirm_clear_data_msg"],
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.unpaid_bills = []
            self.paid_bills = []
            self.budget = 0.0
            self.save_data()
            self.update_display()
            QMessageBox.information(self, STRINGS["info_data_cleared"], STRINGS["info_data_cleared_msg"])
    
    # Security Methods
    def is_locked_out(self):
        """Check if user is currently locked out due to failed PIN attempts."""
        if self.lockout_until is None:
            return False
        if datetime.now() < self.lockout_until:
            return True
        # Lockout expired, reset
        self.lockout_until = None
        self.failed_pin_attempts = 0
        return False
    
    def record_failed_pin(self):
        """Record a failed PIN attempt and trigger lockout if threshold reached."""
        self.failed_pin_attempts += 1
        if self.failed_pin_attempts >= self.max_pin_attempts:
            self.lockout_until = datetime.now() + timedelta(seconds=self.lockout_duration)
            return True  # Locked out
        return False  # Not locked out yet
    
    def reset_pin_attempts(self):
        """Reset failed PIN attempts counter (called on successful PIN entry)."""
        self.failed_pin_attempts = 0
        self.lockout_until = None
    
    def get_remaining_attempts(self):
        """Get number of remaining PIN attempts before lockout."""
        return max(0, self.max_pin_attempts - self.failed_pin_attempts)
    
    def lock_app(self, silent=False):
        """Lock the application and require PIN to unlock."""
        # Allow checking if PIN enabled even if session_pin is missing (Startup Login Mode)
        pin_enabled = self.data_manager.security.get('pin_enabled', False)
        if not self.session_pin and not pin_enabled:
            return

        # If already locked...
        if self.is_locked:
            # If silent request (minimize) or already prompting, ignore
            if silent or self.is_prompting:
                return

        self.is_locked = True
        self.hide()  # Hide main window
        
        if silent:
            return

        self.is_prompting = True
        try:
            # Show PIN entry dialog
            while self.is_locked:
                if self.is_locked_out():
                    lockout_time = self.lockout_until.strftime("%H:%M:%S")
                    QMessageBox.warning(
                        None,
                        STRINGS["msg_too_many_attempts"],
                        STRINGS["msg_locked_out_until"].format(time=lockout_time)
                    )
                    # Wait a bit before checking again
                    QTimer.singleShot(5000, lambda: None)
                    continue
                
                # Pass can_minimize=True so user can re-minimize from lock screen
                # Also pass the PIN hint if it exists
                pin_hint = self.data_manager.security.get('pin_hint')
                dialog = PinEntryDialog(None, mode='verify', can_minimize=True, hint=pin_hint)
                dialog.setWindowTitle(STRINGS["msg_app_locked"])
                dialog.label.setText(STRINGS["msg_enter_pin_unlock"])
                
                # Show remaining attempts if some have failed
                if self.failed_pin_attempts > 0:
                    remaining = self.get_remaining_attempts()
                    dialog.label.setText(
                        f"{STRINGS['msg_enter_pin_unlock']}\n" +
                        STRINGS["msg_attempts_remaining"].format(count=remaining)
                    )
                
                result = dialog.exec()
                if result == QDialog.DialogCode.Accepted:
                    entered_pin = dialog.pin_input.text()
                    
                    # Verify PIN (Session or Hash for Login Mode)
                    is_valid = False
                    if self.session_pin:
                        is_valid = (entered_pin == self.session_pin)
                    else:
                         # Startup/Login Mode: Verify against stored hash
                         stored_hash = self.data_manager.security.get('pin_hash')
                         if stored_hash:
                             is_valid = (hashlib.sha256(entered_pin.encode()).hexdigest() == stored_hash)
                    
                    if is_valid:
                        self.reset_pin_attempts()
                        
                        # If in Login Mode, set session pin and reload full config/data
                        if not self.session_pin:
                            self.session_pin = entered_pin
                            # Reload config with PIN
                            config = self.data_manager.load_config(self.session_pin)
                            # Update Data Path if custom
                            if 'data_file_path' in config:
                                self.data_manager.data_file = config['data_file_path']
                            # Load Bill Data
                            self.load_data()
                            self.update_display()
                        
                        self.is_locked = False
                        self.show_window() # Correctly restore window state
                        self.last_activity_time = datetime.now()  # Reset idle timer
                        break
                    else:
                        locked_out = self.record_failed_pin()
                        if locked_out:
                            continue  # Will show lockout message on next iteration
                        else:
                            remaining = self.get_remaining_attempts()
                            QMessageBox.warning(
                                None,
                                STRINGS["dialog_input_error"],
                                STRINGS["msg_attempts_remaining"].format(count=remaining)
                            )
                elif result == 102:
                     # User wants to minimize back to tray
                     # Keep is_locked = True, hide window (already hidden), break loop
                     break
                else:
                    # User cancelled (X), check if we should exit?
                    # PinEntryDialog.closeEvent handles Exit/Minimize prompt.
                    # If we are here, it means 'Reject' (0) -> Cancel -> Loop continues?
                    # No, logic was: cancel -> keep locked -> break loop?
                    # Standard behavior: break loop, keep locked, app hidden.
                    # User must click Tray again.
                    break
        finally:
            self.is_prompting = False

    def unlock_app(self):
        """Unlock the application."""
        self.is_locked = False
        self.show_window()
        self.last_activity_time = datetime.now()
    
    def check_idle_timeout(self):
        """Check if idle timeout has been reached and lock if necessary."""
        try:
            if not self.auto_lock_enabled or not self.session_pin or self.is_locked:
                return
            
            idle_seconds = (datetime.now() - self.last_activity_time).total_seconds()
            timeout_min = int(self.idle_timeout_minutes)
            
            # Debug: print(f"Idle: {idle_seconds:.1f}s / {timeout_min*60}s")
            
            if idle_seconds >= (timeout_min * 60):
                print(f"Auto-lock triggered. Idle for {idle_seconds:.1f}s")
                self.lock_app()
        except Exception as e:
            print(f"Auto-lock check error: {e}")
    
    def reset_idle_timer(self):
        """Reset the idle timer (called on user activity)."""
        self.last_activity_time = datetime.now()
    
    def eventFilter(self, obj, event):
        """Track user activity for auto-lock."""
        # Track mouse and keyboard events as activity
        if event.type() in [event.Type.MouseButtonPress, event.Type.KeyPress, 
                           event.Type.MouseMove, event.Type.Wheel]:
            self.reset_idle_timer()
        return super().eventFilter(obj, event)
    
    def closeEvent(self, event):
        """Handle window close event with user choice."""
        self.save_data()
        
        # If already marked for real close (from quit_app), just close
        if self.real_close:
            event.accept()
            return
        
        # Check if "Minimize to Tray" is enabled
        if self.minimize_to_tray:
            # Silent minimize to tray
            event.ignore()
            self.hide_to_tray()
        else:
            # Minimize to tray disabled, quit the app
            self.quit_app()

    def hide_to_tray(self):
        """Minimize the application to the system tray."""
        self.hide()
        
        # Lock if "Lock on Minimize" is enabled and we have a PIN set
        if self.session_pin and self.lock_on_minimize:
            self.lock_app(silent=True)
            
        if self.tray_icon.isSystemTrayAvailable():
            self.tray_icon.showMessage(
                "BillTracker",
                STRINGS.get("msg_running_background", "Running in background"),
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )

    def quit_app(self):
        """Properly quit the application."""
        self.real_close = True
        self.tray_icon.hide()  # Hide tray icon before quitting
        QApplication.quit()  # Properly quit the application

    def show_window(self):
        if self.is_locked:
            self.lock_app(silent=False)
            if self.is_locked: # User checked cancel
                return

        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowState.WindowMinimized | Qt.WindowState.WindowActive)
        self.activateWindow()

    def show_bill_details(self, item, is_paid=False):
        """Show details dialog for double-clicked bill."""
        if not item: return
        bill = item.data(Qt.ItemDataRole.UserRole)
        # Verify it's a dict (bill object) and not just a string/int
        if not isinstance(bill, dict): return
        
        dialog = BillDetailsDialog(self, bill, self.currencies, is_paid)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            action = dialog.get_action()
            if action == 1: # Pay
                self.pay_bill(bill)
            elif action == 2: # Edit
                self.edit_bill(bill)
            elif action == 3: # Delete
                self.delete_bill(bill)

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.show_window()

    def open_search(self):
        """Open the global search dialog."""
        searchDialog = SearchDialog(self, self.unpaid_bills, self.paid_bills, self.currencies)
        searchDialog.exec()

    def open_currency_search(self, combo_box):
        """Open searchable currency selector for a combo box (Global)."""
        dialog = CurrencySelectorDialog(self, self.currencies, combo_box.currentText())
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected = dialog.get_selected_currency()
            if selected:
                # Ensure it's in the list (v6.7.4)
                if combo_box.findText(selected) == -1:
                    combo_box.addItem(selected)
                
                if hasattr(combo_box, 'ensure_populated'):
                    combo_box.ensure_populated()
                combo_box.setCurrentText(selected)
    
    def quick_add_bill(self):
        """Open add bill dialog from anywhere using Ctrl+N."""
        # Switch to Dashboard tab where the add bill form is
        self.tabs.setCurrentIndex(0)
        # Focus on the bill name input
        if hasattr(self, 'bill_name_input'):
            self.bill_name_input.setFocus()


    




class SingleInstanceChecker:
    def __init__(self, key):
        self.key = key
        self.server = QLocalServer()
        self.socket = QLocalSocket()
        self.socket.connectToServer(self.key)
        
    def is_running(self):
        if self.socket.waitForConnected(500):
            # Already running - tell the other instance to show itself
            self.socket.write(b"SHOW_WINDOW")
            self.socket.waitForBytesWritten(500)
            return True
        return False

    def start_server(self, window_callback):
        # Remove any existing server file if it exists
        QLocalServer.removeServer(self.key)
        self.server.listen(self.key)
        self.server.newConnection.connect(lambda: self._handle_new_connection(window_callback))

    def _handle_new_connection(self, window_callback):
        socket = self.server.nextPendingConnection()
        if socket.waitForReadyRead(500):
            data = socket.readAll().data().decode()
            if data == "SHOW_WINDOW":
                window_callback()
        socket.disconnectFromServer()

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication, QStyleFactory
    # Taskbar icon fix
    myappid = 'grouvya.billtracker.qt.5.3.0'
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except:
        pass

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False) # v6.2.1: Prevent quitting when main hides for Mini Mode
    
    # 0. Single Instance Check
    checker = SingleInstanceChecker("grouvya.billtracker.qt.singleinstance.v5.16.1")
    if checker.is_running():
        sys.exit(0)
    
    # Apply initial theme (Dark by default for splash and selector)
    set_theme(ThemeManager())

    # 1. Check for First Run (Language Selection)
    config_dir = os.path.join(os.path.expanduser('~'), '.bill_tracker')
    config_file = os.path.join(config_dir, 'config.json')
    
    if not os.path.exists(config_file):
        # First run! Show language selector
        selector = LanguageSelectionDialog(accent_color=ThemeManager().accent_color)
        if selector.exec() == QDialog.DialogCode.Accepted:
            selected_lang = selector.selected_language
            # Save the initial config immediately
            os.makedirs(config_dir, exist_ok=True)
            initial_cfg = {
                'language': selected_lang,
                'minimize_to_tray': False,
                'reminder_days': 1,
                'dark_mode': True
            }
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(initial_cfg, f, indent=4)
            
            # Apply language
            if selected_lang in TRANSLATIONS:
                STRINGS = SafeStrings(selected_lang)
                CATEGORIES = STRINGS["categories_list"]
                FREQUENCIES = STRINGS["frequencies_list"]
        else:
            sys.exit(0) # User cancelled
    # Load Existing Language Preference
    pin_hash = None
    pin_enabled = False
    
    # Load Security Preference (PIN Check)
    config_dir = os.path.join(os.path.expanduser('~'), '.bill_tracker')
    security_file = os.path.join(config_dir, 'security.json')
    
    # Use DataManager to load security (handles multiple layers of encryption/obfuscation)
    try:
        temp_dm = DataManager(config_dir)
        # DataManager.init automatically loads security.json (migrating/decrypting if needed)
        # So we can just read from temp_dm.security
        pin_hash = temp_dm.security.get('pin_hash')
        pin_enabled = temp_dm.security.get('pin_enabled', False)
        
        # KEY FIX: Read language from security metadata (unencrypted) if available
        # This ensures PIN dialog is localized even if config.json is encrypted
        security_lang = temp_dm.security.get('language')
        if security_lang and security_lang in TRANSLATIONS:
             STRINGS = SafeStrings(security_lang)
             CATEGORIES = STRINGS["categories_list"]
             FREQUENCIES = STRINGS["frequencies_list"]
        else:
            # Also check for language in config (might be encrypted, so we might fail to read it here)
            # If encrypted, we default to English until we have PIN (unless security_lang found above)
            config = temp_dm.load_config(None) # Try unencrypted load
            lang = config.get('language', 'English')
            if lang in TRANSLATIONS:
                STRINGS = SafeStrings(lang)
                CATEGORIES = STRINGS["categories_list"]
                FREQUENCIES = STRINGS["frequencies_list"]
            
    except Exception as e:
        print(f"Error initializing security: {e}")
        # Fallback to defaults
                    
        # Load language
        if os.path.exists(config_file):
             # Try load lang from config (might be encrypted, default English)
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    cfg = json.load(f)
                    lang = cfg.get('language', 'English')
                    if lang in TRANSLATIONS:
                        STRINGS = SafeStrings(lang)
                        CATEGORIES = STRINGS["categories_list"]
                        FREQUENCIES = STRINGS["frequencies_list"]
            except:
                pass 
                
    except Exception as e:
        print(f"Error loading configuration: {e}")
    # PIN Security Check 🛡️
    session_pin = None
    start_minimized = False
    
    if pin_enabled and pin_hash:
        # Load lockout state
        config_dir = os.path.join(os.path.expanduser('~'), '.bill_tracker')
        temp_dm = DataManager(config_dir)
        failed_attempts, lockout_until = temp_dm.load_lockout_state()
        
        while True:
            # Check if locked out
            if lockout_until and datetime.now() < lockout_until:
                lockout_time = lockout_until.strftime("%H:%M:%S")
                QMessageBox.critical(
                    None, 
                    STRINGS["msg_too_many_attempts"],
                    STRINGS["msg_lockout_wait"].format(time=lockout_time)
                )
                sys.exit(0)
            elif lockout_until and datetime.now() >= lockout_until:
                # Lockout expired, reset
                temp_dm.clear_lockout_state()
                failed_attempts = 0
            
            # Show PIN dialog with Minimize Option
            pin_dialog = PinEntryDialog(mode='verify', can_minimize=True)
            result = pin_dialog.exec()
            
            if result == QDialog.DialogCode.Accepted:
                session_pin = pin_dialog.pin_input.text().strip()
                if hashlib.sha256(session_pin.encode()).hexdigest() != pin_hash:
                    # Wrong PIN - record failed attempt
                    failed_attempts += 1
                    if failed_attempts >= 5:  # Max attempts
                        lockout_until = datetime.now() + timedelta(seconds=300)  # 5 minutes
                        temp_dm.save_lockout_state(failed_attempts, lockout_until)
                        QMessageBox.critical(
                            None, 
                            STRINGS["msg_too_many_attempts"], 
                            STRINGS["msg_lockout_new"].format(time=lockout_until.strftime('%H:%M:%S'))
                        )
                    else:
                        temp_dm.save_lockout_state(failed_attempts, None)
                        remaining = 5 - failed_attempts
                        QMessageBox.critical(
                            None, 
                            STRINGS["title_access_denied"], 
                            STRINGS["msg_pin_fail_exit"].format(count=remaining)
                        )
                    sys.exit(0)
                else:
                    # Correct PIN - clear lockout
                    temp_dm.clear_lockout_state()
                    break # Proceed to launch
            
            elif result == 102:
                # Minimize request (Start in Background)
                # Ensure we have defaults if we minimize without PIN
                start_minimized = True
                break
            
            else:
                # Exit
                sys.exit(0)

    app.setWindowIcon(QIcon(resource_path('calc.ico')))
    
    # Initialize Main Window (session_pin might be None if minimized)
    window = BillTrackerWindow(session_pin)
    
    if start_minimized:
        # Skip Splash, start server, go to tray
        # IMPORTANT: hide_to_tray will call lock_app(silent=True) ONLY if session_pin is set?
        # No, we updated hide_to_tray logic?
        # hide_to_tray checks: if self.session_pin and self.lock_on_minimize
        # Here session_pin is None. So hide_to_tray just calls self.hide().
        # But we WANT it locked.
        # Window starts with is_locked=False by default.
        # We must explicitly lock it.
        # And because session_pin is None, lock_app (refactored) will work in "Login Mode".
        
        checker.start_server(window.show_window)
        window.hide_to_tray()
        
        # Manually force lock because hide_to_tray might skip it if session_pin is None
        window.lock_app(silent=True)
        
    else:
        # Standard Splash Screen Launch
        splash = SplashScreen(ThemeManager().accent_color)
        splash.show()
        app.processEvents()
        
        # Simulate initialization with progress updates
        splash.update_progress(10, STRINGS["msg_loading_config"])
        QTimer.singleShot(100, lambda: None)  # Small delay for visual effect
        app.processEvents()
        
        splash.update_progress(30, STRINGS["msg_init_security"])
        QTimer.singleShot(100, lambda: None)
        app.processEvents()
        
        splash.update_progress(50, STRINGS["msg_loading_rates"])
        QTimer.singleShot(100, lambda: None)
        app.processEvents()
        
        splash.update_progress(70, STRINGS["msg_prep_interface"])
        checker.start_server(window.show_window)
        app.processEvents()
        
        splash.update_progress(90, STRINGS["msg_finalizing"])
        QTimer.singleShot(100, lambda: None)
        app.processEvents()
        
        splash.update_progress(100, "Ready!")
        
        # Close splash and show main window
        QTimer.singleShot(500, splash.close)
        
        # Only show window if we have a PIN (or PIN disabled), otherwise start locked?
        # If we broke loop with Valid PIN -> session_pin is set -> Just show.
        # If PIN disabled -> session_pin None -> Just show.
        QTimer.singleShot(600, window.show_window)
    
    sys.exit(app.exec())
