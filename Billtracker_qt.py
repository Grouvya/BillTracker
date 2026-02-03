
#!/usr/bin/env python3
# Bill & Savings Tracker - PyQt6 Version (Windows Compatible Modern GUI)
# Version 5.5.0 Cross-Platform
# To run: pip install PyQt6

__version__ = '5.5.0 Cross-Platform'

import sys
import os
import json
from datetime import datetime, date
import threading
import webbrowser
import urllib.request
import ssl
import ctypes
import hashlib
import shutil
import csv
import platform  # For cross-platform detection

# Platform-specific imports
if platform.system() == 'Windows':
    import winreg  # For Start with Windows (Windows only)

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

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox,
    QMessageBox, QDialog, QFormLayout, QDateEdit, QFileDialog, QProgressBar, QScrollArea, QListWidget,
    QListWidgetItem, QGroupBox, QGridLayout, QDoubleSpinBox, QInputDialog, QListWidgetItem as ListItem,
    QMenu, QAbstractItemView, QGraphicsDropShadowEffect, QGraphicsBlurEffect, QSystemTrayIcon, QTabWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QCalendarWidget
)
from PyQt6.QtCore import Qt, QTimer, QDate, QThread, pyqtSignal, QPoint, QRectF, QRect
from PyQt6.QtGui import QFont, QColor, QAction, QIcon, QPalette, QPainter, QPen, QBrush
from PyQt6.QtWidgets import QComboBox as _QComboBox

STRINGS = {
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
    "donate_button": "Donate",
    "refresh_rates_button": "Refresh Rates",
    "settings_button": "Settings",
    "unpaid_bills_title": "Unpaid Bills",
    "sort_name_button": "Name",
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
    "notification_title": "Bills Due Soon",
    "notification_msg": "You have {} bills due today or tomorrow!",
}

CATEGORIES = ["Housing", "Utilities", "Food", "Transport", "Subscription", "Debt", "Healthcare", "Personal", "Other"]
FREQUENCIES = ["No Repeat", "Weekly", "Monthly", "Yearly"]

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
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_icon_path():
    """Get platform-appropriate icon path."""
    if platform.system() == 'Windows':
        return resource_path('billtracker.ico')
    else:
        # macOS and Linux use PNG
        return resource_path('billtracker.png')





# Security Utilities
def sanitize_input(text, max_length=100):
    """Sanitize user input to prevent injection and display issues."""
    if not isinstance(text, str):
        return ""
    # Remove control characters, keep printable + newline/tab
    sanitized = ''.join(c for c in text if c.isprintable() or c in '\n\r\t')
    return sanitized[:max_length]

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
        os.makedirs(self.config_dir, exist_ok=True)




    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.data_file = config.get('data_file_path', self.data_file)
                    return config
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def save_config(self, config_data):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4)
        except IOError as e:
            print(f"Error saving config: {e}")

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                # Security: Check file size (max 10MB to prevent DoS)
                file_size = os.path.getsize(self.data_file)
                if file_size > 10 * 1024 * 1024:
                    logging.error(f"Data file too large: {file_size} bytes (max 10MB)")
                    return {}
                
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    content = f.read(10 * 1024 * 1024)  # Max 10MB read
                
                # Integrity Check
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
                    return {}
                # Basic schema validation
                safe_data = {}
                safe_data['budget'] = float(data.get('budget', 0.0))
                safe_data['unpaid_bills'] = [b for b in data.get('unpaid_bills', []) if isinstance(b, dict) and 'name' in b and 'amount' in b]
                safe_data['paid_bills'] = [b for b in data.get('paid_bills', []) if isinstance(b, dict) and 'name' in b and 'amount' in b]
                safe_data['budget_currency'] = str(data.get('budget_currency', '$ (USD)'))
                safe_data['bill_currency'] = str(data.get('bill_currency', '$ (USD)'))
                safe_data['summary_currency'] = str(data.get('summary_currency', '$ (USD)'))
                
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

    def save_data(self, data_to_save):
        try:
            # Prepare data
            json_str = json.dumps(data_to_save, indent=4, ensure_ascii=False)
            
            # 1. Integrity: Calculate and Save Hash
            data_hash = hashlib.sha256(json_str.encode('utf-8')).hexdigest()
            hash_file = self.data_file + ".sha256"
            with open(hash_file, 'w', encoding='utf-8') as f:
                f.write(data_hash)

            # 2. Atomic Write
            tmp_file = self.data_file + ".tmp"
            with open(tmp_file, 'w', encoding='utf-8') as f:
                f.write(json_str)
            
            # Atomic swap
            os.replace(tmp_file, self.data_file)
            
            # Backup after successful save
            self.backup_data()
            
        except IOError as e:
            print(f"Error saving data: {e}")

    def backup_data(self):
        """Create a rotating backup of the data file."""
        if not os.path.exists(self.data_file):
            return
            
        try:
            backup_dir = os.path.join(self.config_dir, 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = os.path.join(backup_dir, f"bill_data_{timestamp}.json")
            
            shutil.copy2(self.data_file, backup_path)
            
            # Rotate: Keep last 5
            backups = sorted([os.path.join(backup_dir, f) for f in os.listdir(backup_dir) if f.startswith('bill_data_')])
            while len(backups) > 5:
                os.remove(backups.pop(0))
        except Exception:
            pass

    def save_rates_cache(self, rates_data):
        try:
            cache_file = os.path.join(self.config_dir, 'rates_cache.json')
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(rates_data, f, indent=2)
        except IOError:
            pass

    def load_rates_cache(self):
        try:
            cache_file = os.path.join(self.config_dir, 'rates_cache.json')
            if os.path.exists(cache_file):
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (IOError, json.JSONDecodeError):
            return None
        return None


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


def get_currency_list():
    """Returns dictionary of currency display strings to symbols."""
    return {
        '$ (USD)': '$', '€ (EUR)': '€', '£ (GBP)': '£', '¥ (JPY)': '¥', 'C$ (CAD)': 'C$',
        'A$ (AUD)': 'A$', '₹ (INR)': '₹', '₽ (RUB)': '₽', '₩ (KRW)': '₩', '₽ (CNY)': '¥',
        'R$ (BRL)': 'R$', 'CHF (CHF)': 'CHF', 'kr (SEK)': 'kr', 'kr (NOK)': 'kr', 'kr (DKK)': 'kr',
        'kr (ISK)': 'kr', 'zł (PLN)': 'zł', 'Kč (CZK)': 'Kč', 'Ft (HUF)': 'Ft', 'lei (RON)': 'lei',
        '₪ (ILS)': '₪', '₼ (AZN)': '₼', '₼ (AZN)': '₼', '₺ (TRY)': '₺', '₱ (PHP)': '₱',
        'Rp (IDR)': 'Rp', 'RM (MYR)': 'RM', 'S$ (SGD)': 'S$', 'NZ$ (NZD)': 'NZ$', 'HK$ (HKD)': 'HK$',
        'NT$ (TWD)': 'NT$', 'Bs. (BOB)': 'Bs.', '₡ (CRC)': '₡', 'RD$ (DOP)': 'RD$', '$ (MXN)': '$',
        '฿ (THB)': '฿', '₫ (VND)': '₫', 'Rp (IDR)': 'Rp', '$ (ARS)': '$', 'S/. (PEN)': 'S/.',
        '₦ (NGN)': '₦', '₨ (PKR)': '₨', '₨ (INR)': '₹', 'Br (ETB)': 'Br', 'KSh (KES)': 'KSh',
        'R (ZAR)': 'R', 'Fdj (DJF)': 'Fdj', 'ر.ع. (AED)': 'د.إ', '﷼ (SAR)': '﷼', 'د (KWD)': 'د.ك',
        'ر (QAR)': 'ر.ق', '﷼ (IRR)': '﷼', 'D (GMD)': 'D', 'Le (SLL)': 'Le'
    }


class LazyCombo(_QComboBox):
    """QComboBox that populates items lazily on first showPopup to speed startup."""
    def __init__(self, items_provider=None, pending_text=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._items_provider = items_provider
        self._populated = False
        self._pending_text = pending_text

    def showPopup(self):
        if not self._populated and self._items_provider:
            items = self._items_provider()
            if items:
                self.addItems(items)
            self._populated = True
            if self._pending_text:
                # try to set pending selection if provided
                try:
                    self.setCurrentText(self._pending_text)
                except Exception:
                    pass
        super().showPopup()


class CurrencySelectorDialog(QDialog):
    """Searchable currency selector dialog."""
    def __init__(self, parent, currencies, current_currency=None):
        super().__init__(parent)
        self.setWindowTitle("Select Currency")
        self.setGeometry(100, 100, 400, 500)
        self.currencies = currencies
        self.selected_currency = current_currency
        
        layout = QVBoxLayout()
        
        # Search input
        search_label = QLabel("Search currency (code, symbol, or name):")
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
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.on_ok)
        cancel_button = QPushButton("Cancel")
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
        
        for currency in self.currencies.keys():
            code = currency.split('(')[-1].replace(')', '').strip()
            name = CURRENCY_FULL_NAMES.get(code, '')
            
            # Search in code, symbol, and name
            if (filter_lower == "" or 
                filter_lower in currency.lower() or 
                filter_lower in code.lower() or 
                filter_lower in name.lower()):
                item = QListWidgetItem(f"{currency} - {name}")
                item.setData(Qt.ItemDataRole.UserRole, currency)
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
        self.currency_combo.addItems(list(currencies.keys()))
        self.currency_combo.setCurrentText(bill['currency'])
        currency_layout.addWidget(self.currency_combo)
        
        search_currency_btn = QPushButton("🔍 Search")
        search_currency_btn.clicked.connect(self.open_currency_selector)
        currency_layout.addWidget(search_currency_btn)
        layout.addRow(STRINGS["currency_label"] + ":", currency_layout)
        
        layout.addRow(STRINGS["category_label"] + ":", self.currency_combo) # Placeholder replacer below
        
        self.category_combo = QComboBox()
        self.category_combo.addItems(CATEGORIES)
        self.category_combo.setCurrentText(bill.get('category', 'Other'))
        layout.addRow(STRINGS["category_label"] + ":", self.category_combo)
        
        self.repeat_combo = QComboBox()
        self.repeat_combo.addItems(FREQUENCIES)
        self.repeat_combo.setCurrentText(bill.get('repeat_freq', 'No Repeat'))
        layout.addRow(STRINGS["repeat_label"] + ":", self.repeat_combo)
        
        self.date_input = QDateEdit()
        try:
            due_date = datetime.strptime(bill['due_date'], '%Y-%m-%d').date()
            self.date_input.setDate(QDate(due_date.year, due_date.month, due_date.day))
        except:
            self.date_input.setDate(QDate.currentDate())
        layout.addRow(STRINGS["due_date_label"] + ":", self.date_input)
        
        save_button = QPushButton(STRINGS["save_changes_button"])
        save_button.clicked.connect(self.accept)
        layout.addRow(save_button)
        
        self.setLayout(layout)
    
    def open_currency_selector(self):
        dialog = CurrencySelectorDialog(self, self.currencies, self.currency_combo.currentText())
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected = dialog.get_selected_currency()
            if selected:
                self.currency_combo.setCurrentText(selected)
    
    def get_data(self):
        try:
            amount = float(self.amount_input.text())
            if amount <= 0:
                raise ValueError
            if amount > 1000000000: # 1 Billion limit
                QMessageBox.warning(self, STRINGS["dialog_input_error"], "Amount is too large.")
                return None
        except ValueError:
            QMessageBox.warning(self, STRINGS["dialog_input_error"], STRINGS["error_positive_amount"])
            return None
        
        return {
            'name': self.name_input.text().strip(),
            'amount': amount,
            'currency': self.currency_combo.currentText(),
            'category': self.category_combo.currentText(),
            'repeat_freq': self.repeat_combo.currentText(),
            'due_date': self.date_input.date().toString('yyyy-MM-dd')
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
        self.from_combo = QComboBox()
        self.from_combo.addItems(list(currencies.keys()))
        self.from_combo.setCurrentText('$ (USD)')
        layout.addWidget(self.from_combo)
        
        # To currency
        layout.addWidget(QLabel(STRINGS["to_label"] + ":"))
        self.to_combo = QComboBox()
        self.to_combo.addItems(list(currencies.keys()))
        self.to_combo.setCurrentText('€ (EUR)')
        layout.addWidget(self.to_combo)
        
        # Result
        self.result_label = QLabel("0.00")
        result_font = QFont()
        result_font.setPointSize(14)
        result_font.setBold(True)
        self.result_label.setFont(result_font)
        layout.addWidget(self.result_label)
        
        # Convert button
        convert_button = QPushButton(STRINGS["convert_button"])
        convert_button.clicked.connect(self.perform_conversion)
        layout.addWidget(convert_button)
        
        copy_button = QPushButton("📋 Copy Result")
        copy_button.clicked.connect(self.copy_result)
        layout.addWidget(copy_button)
        
        self.setLayout(layout)
    
    def perform_conversion(self):
        try:
            amount = float(self.amount_input.text())
            from_curr = self.from_combo.currentText()
            to_curr = self.to_combo.currentText()
            
            from_rate = self.exchange_rates.get(from_curr, 1)
            to_rate = self.exchange_rates.get(to_curr, 1)
            
            if from_rate > 0:
                result = (amount / from_rate) * to_rate
                symbol = self.currencies.get(to_curr, '$')
                self.result_label.setText(f"{symbol}{result:,.2f}")
            else:
                self.result_label.setText("Error")
        except ValueError:
            self.result_label.setText("Invalid Input")

    def copy_result(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.result_label.text())
        QMessageBox.information(self, "Copied", "Result copied to clipboard!")


class SettingsDialog(QDialog):
    """Settings dialog."""
    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.data_manager = data_manager
        self.setWindowTitle(STRINGS["settings_title"])
        self.setGeometry(100, 100, 500, 200)
        
        layout = QFormLayout()
        
        # Data file path
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit(data_manager.data_file)
        self.path_input.setReadOnly(True)
        path_layout.addWidget(self.path_input)
        
        browse_button = QPushButton(STRINGS["browse_button"])
        browse_button.clicked.connect(self.browse_file)
        path_layout.addWidget(browse_button)
        
        layout.addRow(STRINGS["data_file_group_title"] + ":", path_layout)
        


        # Create Start with Windows checkbox
        self.start_boot_chk = QCheckBox("Start with Windows")
        self.start_boot_chk.setChecked(self.is_run_on_startup())
        layout.addRow(self.start_boot_chk)
        
        # Create Minimize to Tray checkbox (saved in config)
        self.tray_chk = QCheckBox("Minimize to Tray on Close")
        config = self.data_manager.load_config()
        self.tray_chk.setChecked(config.get('minimize_to_tray', True))
        layout.addRow(self.tray_chk)

        # Save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        layout.addRow(save_button)
        
        self.setLayout(layout)
    
    def browse_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Choose data file", "", "JSON Files (*.json)")
        if file_path:
            self.path_input.setText(file_path)
            # We don't save immediately here to allow 'Save' button to handle everything
            
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
                logging.warning(f"Registry check error: {e}")
                return False
        
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
                if enable:
                    app_path = sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]
                    winreg.SetValueEx(key, "BillTracker", 0, winreg.REG_SZ, app_path)
                else:
                    try:
                        winreg.DeleteValue(key, "BillTracker")
                    except FileNotFoundError:
                        pass
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

    def save_settings(self):
        # Save Data Path with validation
        new_path = self.path_input.text()
        if new_path and new_path != self.data_manager.data_file:
            # Validate path for security
            if not validate_file_path(new_path):
                QMessageBox.warning(self, "Invalid Path", 
                    "For security reasons, data files must be stored in your user directory.\n"
                    "System directories are not allowed.")
                return
            
            self.data_manager.data_file = new_path
            config = self.data_manager.load_config()
            config['data_file_path'] = new_path
            self.data_manager.save_config(config)

        # Save Tray Setting
        config = self.data_manager.load_config()
        config['minimize_to_tray'] = self.tray_chk.isChecked()
        self.data_manager.save_config(config)

        # Save Registry with enhanced error handling
        try:
            self.set_run_on_startup(self.start_boot_chk.isChecked())
        except PermissionError:
            QMessageBox.warning(self, "Permission Denied", 
                "Administrator rights required to modify startup settings.")
        except Exception as e:
            QMessageBox.critical(self, "Registry Error", 
                f"Failed to update startup settings: {str(e)}")
        
        self.accept()


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
        save_action = menu.addAction("💾 Save Chart as Image")
        action = menu.exec(event.globalPos())
        if action == save_action:
            self.save_image()

    def save_image(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Chart", "chart.png", "Images (*.png *.jpg *.bmp)")
        if file_path:
            pixmap = self.grab()
            pixmap.save(file_path)
            QMessageBox.information(self, "Saved", f"Chart saved to {file_path}")

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
            painter.setBrush(QColor("#8338ec"))
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


class SplashScreen(QWidget):
    """Modern loading screen with progress indicator."""
    def __init__(self):
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
        title = QLabel("💰 BillTracker")
        title.setStyleSheet("font-size: 36px; font-weight: bold; color: #8338ec; background: transparent;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Version
        version = QLabel(f"v{__version__}")
        version.setStyleSheet("font-size: 14px; color: #aaaaaa; background: transparent;")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Loading message
        self.message = QLabel("Initializing...")
        self.message.setStyleSheet("font-size: 14px; color: #ffffff; background: transparent;")
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 5px;
                background-color: rgba(255, 255, 255, 0.1);
                height: 8px;
            }
            QProgressBar::chunk {
                border-radius: 5px;
                background-color: #8338ec;
            }
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


class BillTrackerWindow(QMainWindow):
    """Main application window."""
    def __init__(self):
        super().__init__()
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
        self.full_currency_list = list(self.currencies.keys())
        self.exchange_rates = {}
        self.unpaid_bills = []
        self.paid_bills = []
        self.budget = 0.0
        self.load_data()
        
        # Load theme preference
        config = self.data_manager.load_config()
        self.is_dark_mode = config.get('dark_mode', False)
        
        # UI Setup
        # Suppress updates while building the UI to avoid repeated repaints
        self.setUpdatesEnabled(False)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Apply initial theme
        self.apply_theme()
        
        # System Tray & Notifications
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(get_icon_path()))
        
        # Tray Menu
        tray_menu = QMenu()
        open_action = tray_menu.addAction("Open")
        open_action.triggered.connect(self.show_window)
        quit_action = tray_menu.addAction("Quit")
        quit_action.triggered.connect(self.quit_app)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_activated)
        
        self.tray_icon.show()
        
        # Background Timer for Reminders (Every 4 hours)
        self.bg_timer = QTimer(self)
        self.bg_timer.timeout.connect(self.check_due_bills)
        self.bg_timer.start(14400000) # 4 hours in ms
        
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
        self.tabs.addTab(self.chart_tab, "📊 Trends")

        # Tab 5: Calendar
        self.calendar_tab = QWidget()
        self.setup_calendar_tab()
        self.tabs.addTab(self.calendar_tab, "📅 Calendar")

        # Tab 6: About
        self.about_tab = QWidget()
        self.setup_about_tab()
        self.tabs.addTab(self.about_tab, "ℹ️ About")

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
        self.rate_timer.start(3600000)  # Every hour
        
        # Connect combo boxes
        self.budget_currency_combo.currentTextChanged.connect(self.update_display)
        self.summary_currency_combo.currentTextChanged.connect(self.update_display)

        # Restore last used currencies
        self.restore_currency_preferences()

        # Re-enable updates after UI construction
        self.setUpdatesEnabled(True)
        
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
        
        # Budget section
        budget_group = QGroupBox(STRINGS["budget_group_title"])
        budget_layout = QHBoxLayout()
        self.budget_input = QLineEdit()
        budget_layout.addWidget(QLabel(STRINGS["budget_row_title"] + ":"))
        budget_layout.addWidget(self.budget_input)
        
        # Use lazy combo to avoid populating all currencies on startup
        self.budget_currency_combo = LazyCombo(items_provider=lambda: self.full_currency_list.copy(), pending_text=None)
        budget_layout.addWidget(self.budget_currency_combo)
        budget_search_btn = QPushButton("🔍 Search")
        budget_search_btn.clicked.connect(lambda: self.open_currency_search(self.budget_currency_combo))
        budget_layout.addWidget(budget_search_btn)
        
        set_budget_btn = QPushButton(STRINGS["set_budget_button"])
        set_budget_btn.clicked.connect(self.set_budget)
        budget_layout.addWidget(set_budget_btn)
        budget_group.setLayout(budget_layout)
        scroll_layout.addWidget(budget_group)
        
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
        self.bill_currency_combo = LazyCombo(items_provider=lambda: self.full_currency_list.copy(), pending_text=None)
        curr_layout.addWidget(self.bill_currency_combo)
        curr_search_btn = QPushButton("🔍")
        curr_search_btn.setFixedWidth(40)
        curr_search_btn.clicked.connect(lambda: self.open_currency_search(self.bill_currency_combo))
        curr_layout.addWidget(curr_search_btn)
        add_bill_layout.addLayout(curr_layout, 2, 1)
        
        # Category
        self.bill_category_combo = QComboBox()
        self.bill_category_combo.addItems(CATEGORIES)
        add_bill_layout.addWidget(QLabel(STRINGS["category_label"] + ":"), 3, 0)
        add_bill_layout.addWidget(self.bill_category_combo, 3, 1)
        
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
        
        add_bill_btn = QPushButton(STRINGS["add_bill_button"])
        add_bill_btn.clicked.connect(self.add_bill)
        add_bill_layout.addWidget(add_bill_btn, 6, 0, 1, 2)
        
        add_bill_group.setLayout(add_bill_layout)
        scroll_layout.addWidget(add_bill_group)
        
        # Summary Area (Quick View)
        summary_group = QGroupBox("Quick Status")
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
        self.summary_currency_combo = LazyCombo(items_provider=lambda: self.full_currency_list.copy(), pending_text=None)
        currency_layout.addWidget(self.summary_currency_combo)
        summary_search_btn = QPushButton("🔍 Search")
        summary_search_btn.clicked.connect(lambda: self.open_currency_search(self.summary_currency_combo))
        currency_layout.addWidget(summary_search_btn)
        summary_layout.addLayout(currency_layout)
        
        summary_group.setLayout(summary_layout)
        scroll_layout.addWidget(summary_group)
        
        # Support & Data (v5.0)
        about_group = QGroupBox("Support & Data")
        about_layout = QVBoxLayout()
        
        # Created By
        credits = QLabel('<a href="https://guns.lol/grouvya" style="color: #8338ec; font-weight: bold; text-decoration: none;">✨ Created by Grouvya! ✨</a>')
        credits.setAlignment(Qt.AlignmentFlag.AlignCenter)
        credits.setOpenExternalLinks(True)
        font = QFont()
        font.setPointSize(11)
        credits.setFont(font)
        about_layout.addWidget(credits)
        
        # Buttons Row
        btn_layout = QHBoxLayout()
        
        donate_btn = QPushButton("☕ Donate")
        donate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        donate_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFDD00; 
                color: black; 
                font-weight: bold;
            }
            QPushButton:hover { background-color: #FFEA00; }
        """)
        donate_btn.clicked.connect(self.open_donation)
        btn_layout.addWidget(donate_btn)
        
        export_btn = QPushButton("📂 Export CSV")
        export_btn.clicked.connect(self.export_csv)
        btn_layout.addWidget(export_btn)
        
        about_layout.addLayout(btn_layout)
        about_group.setLayout(about_layout)
        scroll_layout.addWidget(about_group)
        
        # Other Actions
        actions_group = QGroupBox(STRINGS["actions_group_title"])
        actions_layout = QHBoxLayout()
        
        converter_btn = QPushButton(STRINGS["converter_button"])
        converter_btn.clicked.connect(self.open_converter)
        actions_layout.addWidget(converter_btn)
        
        settings_btn = QPushButton(STRINGS["settings_button"])
        settings_btn.clicked.connect(self.open_settings)
        actions_layout.addWidget(settings_btn)
        
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
        self.unpaid_summary_label = QLabel("Total Unpaid: $0.00")
        self.unpaid_summary_label.setObjectName("summaryLabel")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.unpaid_summary_label.setFont(font)
        self.unpaid_summary_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.unpaid_summary_label)
        
        # Table
        self.unpaid_table = QTableWidget()
        self.unpaid_table.setColumnCount(5)
        self.unpaid_table.setHorizontalHeaderLabels(["Name", "Amount", "Category", "Due Date", "Frequency"])
        self.unpaid_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.unpaid_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.unpaid_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.unpaid_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.unpaid_table.customContextMenuRequested.connect(self.show_unpaid_context_menu)
        layout.addWidget(self.unpaid_table)

    def setup_paid_tab(self):
        layout = QVBoxLayout()
        self.paid_tab.setLayout(layout)
        
        # Summary Header
        self.paid_summary_label = QLabel("Total Paid: $0.00")
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
        self.paid_table.setHorizontalHeaderLabels(["Name", "Amount", "Category", "Paid Date", "Frequency"])
        self.paid_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.paid_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.paid_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.paid_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.paid_table.customContextMenuRequested.connect(self.show_paid_context_menu)
        layout.addWidget(self.paid_table)
    
    def restore_currency_preferences(self):
        """Restore last used currency selections from saved data."""
        try:
            data = self.data_manager.load_data()
            budget_curr = data.get('budget_currency', '$ (USD)')
            bill_curr = data.get('bill_currency', '$ (USD)')
            summary_curr = data.get('summary_currency', '$ (USD)')
            
            if budget_curr in self.full_currency_list:
                self.budget_currency_combo.setCurrentText(budget_curr)
            if bill_curr in self.full_currency_list:
                self.bill_currency_combo.setCurrentText(bill_curr)
            if summary_curr in self.full_currency_list:
                self.summary_currency_combo.setCurrentText(summary_curr)
        except:
            pass
    
    def open_currency_search(self, combo_box):
        """Open searchable currency selector for a combo box."""
        dialog = CurrencySelectorDialog(self, self.currencies, combo_box.currentText())
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected = dialog.get_selected_currency()
            if selected:
                combo_box.setCurrentText(selected)
    
    def load_data(self):
        data = self.data_manager.load_data()
        
        if data.get('__tampered__'):
            reply = QMessageBox.critical(self, "Security Alert", 
                                       "Data Integrity Violation!\n\nThe data file has been modified externally.\nThis could be due to tampering or corruption.\n\nDo you want to restore from the last automatic backup?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.restore_backup()
                return
        
        self.unpaid_bills = data.get('unpaid_bills', [])
        self.paid_bills = data.get('paid_bills', [])
        self.budget = float(data.get('budget', 0.0))
    
    def restore_backup(self):
        """Attempt to restore from backup folder."""
        backup_dir = os.path.join(self.data_manager.config_dir, 'backups')
        if not os.path.exists(backup_dir):
            QMessageBox.warning(self, "Restore Failed", "No backups found.")
            return

        backups = sorted([f for f in os.listdir(backup_dir) if f.startswith('bill_data_')], reverse=True)
        if not backups:
            QMessageBox.warning(self, "Restore Failed", "No backups found.")
            return
            
        latest = os.path.join(backup_dir, backups[0])
        try:
            # Copy backup to main data file
            import shutil
            shutil.copy2(latest, self.data_manager.data_file)
            QMessageBox.information(self, "Restored", f"Restored data from {backups[0]}.\nPlease restart the application.")
            sys.exit(0)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to restore backup: {e}")
    
    def save_data(self):
        data = {
            'budget': self.budget,
            'unpaid_bills': self.unpaid_bills,
            'paid_bills': self.paid_bills,
            'budget_currency': self.budget_currency_combo.currentText(),
            'bill_currency': self.bill_currency_combo.currentText(),
            'summary_currency': self.summary_currency_combo.currentText()
        }
        self.data_manager.save_data(data)
    
    def set_budget(self):
        try:
            amount = float(self.budget_input.text())
            curr = self.budget_currency_combo.currentText()
            rate = self.exchange_rates.get(curr, 1)
            if rate <= 0:
                raise ValueError
            self.budget = amount / rate
            self.save_data()
            QMessageBox.information(self, STRINGS["info_budget_set"], 
                                  STRINGS["info_budget_set_to"].format(f"{self.currencies.get(curr, '')}{amount:,.2f}"))
            self.update_display()
        except ValueError:
            QMessageBox.warning(self, STRINGS["dialog_input_error"], STRINGS["error_valid_number"])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to set budget: {e}")
    
    def add_bill(self):
        name = self.bill_name_input.text().strip()
        amount_text = self.bill_amount_input.text()
        currency = self.bill_currency_combo.currentText()
        category = self.bill_category_combo.currentText()
        repeat = self.bill_repeat_combo.currentText()
        due_date = self.bill_date_input.date().toString('yyyy-MM-dd')
        
        if not name or not amount_text:
            QMessageBox.warning(self, STRINGS["dialog_input_error"], STRINGS["error_enter_name_amount"])
            return
            
        if len(name) > 100:
            QMessageBox.warning(self, STRINGS["dialog_input_error"], "Bill name is too long (max 100 chars).")
            return
        
        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError
            if amount > 1000000000:
                QMessageBox.warning(self, STRINGS["dialog_input_error"], "Amount is too large.")
                return
        except ValueError:
            QMessageBox.warning(self, STRINGS["dialog_input_error"], STRINGS["error_positive_amount"])
            return
        except Exception:
            QMessageBox.warning(self, STRINGS["dialog_input_error"], "Invalid input format.")
            return
        
        bill = {
            'name': name, 
            'amount': amount, 
            'currency': currency, 
            'category': category,
            'repeat_freq': repeat,
            'due_date': due_date,
            'created_at': datetime.now().isoformat()
        }
        self.unpaid_bills.append(bill)
        
        # Reset inputs
        self.bill_name_input.clear()
        self.bill_amount_input.clear()
        
        self.save_data()
        self.update_display()

    def pay_bill(self, bill):
        """Pay a bill and move to paid list. Handle recurrence."""
        reply = QMessageBox.question(self, STRINGS["dialog_confirm_payment"],
                                   STRINGS["confirm_payment_msg"].format(bill['name']),
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            rate = self.exchange_rates.get(bill['currency'], 1)
            # Find closest rate or default
            
            # Handle Recurrence
            freq = bill.get('repeat_freq', 'No Repeat')
            if freq != 'No Repeat':
                try:
                    # Use QDate for robust date math
                    qd = QDate.fromString(bill['due_date'], 'yyyy-MM-dd')
                    if not qd.isValid():
                        qd = QDate.currentDate()
                    
                    if freq == 'Weekly': qd = qd.addDays(7)
                    elif freq == 'Monthly': qd = qd.addMonths(1)
                    elif freq == 'Yearly': qd = qd.addYears(1)
                    
                    new_bill = bill.copy()
                    new_bill['due_date'] = qd.toString('yyyy-MM-dd')
                    new_bill['created_at'] = datetime.now().isoformat()
                    
                    # Auto-create next bill
                    self.unpaid_bills.append(new_bill)
                    
                    # Notify user
                    self.tray_icon.showMessage("Recurring Bill Created", 
                                             f"Next {bill['name']} due on {new_bill['due_date']}",
                                             QSystemTrayIcon.MessageIcon.Information, 3000)
                except Exception as e:
                    print(f"Recurrence error: {e}")

            if bill in self.unpaid_bills:
                self.unpaid_bills.remove(bill)
            self.paid_bills.insert(0, bill) # Add to top
            self.save_data()
            self.update_display()

    def open_donation(self):
        webbrowser.open("https://ko-fi.com/grouvya") # Placeholder or specific link

    def export_csv(self):
        """Export data to CSV."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Data", "bill_history.csv", "CSV Files (*.csv)")
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
            
            QMessageBox.information(self, "Export Successful", f"Data exported to {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", str(e))

    def check_due_bills(self):
        """Check for bills due today or tomorrow."""
        today = date.today()
        count = 0
        for bill in self.unpaid_bills:
            try:
                due = datetime.strptime(bill['due_date'], '%Y-%m-%d').date()
                delta = (due - today).days
                if 0 <= delta <= 1:
                    count += 1
            except: pass
            
        if count > 0:
            self.tray_icon.showMessage(
                STRINGS["notification_title"],
                STRINGS["notification_msg"].format(count),
                QSystemTrayIcon.MessageIcon.Information,
                5000
            )
    
    def refresh_rates(self):
        self.api_thread = APIThread()
        self.api_thread.finished.connect(self.handle_api_result)
        self.api_thread.start()
    
    def handle_api_result(self, result):
        if result['status'] == 'success':
            data = result['data']
            api_rates = data.get('conversion_rates', {})
            updated_rates = {}
            for curr_str in self.currencies:
                code = curr_str.split('(')[-1].replace(')', '').strip()
                if code in api_rates:
                    updated_rates[curr_str] = api_rates[code]
            updated_rates['$ (USD)'] = 1.0
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
        vbox.addWidget(QLabel("Monthly Spending History"))
        self.trends_chart = TrendsWidget()
        vbox.addWidget(self.trends_chart)

    def setup_calendar_tab(self):
        layout = QVBoxLayout()
        self.calendar_tab.setLayout(layout)
        
        self.calendar = BillCalendar()
        self.calendar.clicked.connect(self.handle_calendar_click)
        layout.addWidget(self.calendar)
        
        self.calendar_label = QLabel("Select a date to see bills.")
        self.calendar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.calendar_label)

    def setup_about_tab(self):
        """Setup About tab with lazy-loaded README content."""
        layout = QVBoxLayout()
        self.about_tab.setLayout(layout)
        
        # Create scrollable text area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        # Text widget for README
        self.about_text_widget = QLabel()
        self.about_text_widget.setWordWrap(True)
        self.about_text_widget.setTextFormat(Qt.TextFormat.MarkdownText)
        self.about_text_widget.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.about_text_widget.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.about_text_widget.setStyleSheet("padding: 20px; font-size: 11pt;")
        self.about_text_widget.setText("Loading...")
        
        scroll.setWidget(self.about_text_widget)
        layout.addWidget(scroll)
        
        # Mark as not loaded yet (lazy loading)
        self.about_loaded = False

    def _load_readme(self):
        """Lazy load README content when About tab is opened."""
        if self.about_loaded:
            return
            
        readme_path = resource_path('README.md')
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
            self.about_text_widget.setText(readme_content)
        except FileNotFoundError:
            self.about_text_widget.setText("# README.md not found\n\nThe README file could not be loaded.")
        except Exception as e:
            self.about_text_widget.setText(f"# Error loading README\n\n{str(e)}")
            logging.error(f"Failed to load README: {e}")
        
        self.about_loaded = True


    def handle_calendar_click(self, date):
        dt = date.toString("yyyy-MM-dd")
        bills = [b['name'] for b in self.unpaid_bills if b.get('due_date') == dt]
        if bills:
            self.calendar_label.setText(f"Due on {dt}: {', '.join(bills)}")
        else:
            self.calendar_label.setText(f"No bills due on {dt}")
        
    def update_charts(self):
        if not hasattr(self, 'budget_chart'):
            return
            
        # 1. Budget vs Expenses
        total_unpaid = 0.0
        budget_curr = self.budget_currency_combo.currentText()
        target_rate = self.exchange_rates.get(budget_curr, 1) or 1
        
        for bill in self.unpaid_bills:
            b_rate = self.exchange_rates.get(bill['currency'], 1) or 1
            if b_rate > 0:
                total_unpaid += (bill['amount'] / b_rate) * target_rate
            
        # Chart Remaining vs Unpaid (Total Budget = Budget + Unpaid?)
        # Logic: self.budget is remaining.
        self.budget_chart.set_data({"Remaining": max(0, self.budget), "Unpaid Bills": total_unpaid})
        
        # 2. Expenses by Category (Unpaid)
        cat_data = {}
        for bill in self.unpaid_bills:
            cat = bill.get('category', 'Other')
            b_rate = self.exchange_rates.get(bill['currency'], 1) or 1
            if b_rate > 0:
                amt = (bill['amount'] / b_rate) * target_rate
                cat_data[cat] = cat_data.get(cat, 0) + amt
            
        self.category_chart.set_data(cat_data)
        
        # 3. Trends (Paid History by Month)
        trends_data = {}
        for bill in self.paid_bills:
            # Assume bill has 'due_date' or we use today if missing
            d = bill.get('due_date', '')
            if len(d) >= 7:
                key = d[:7] # YYYY-MM
                b_rate = self.exchange_rates.get(bill['currency'], 1) or 1
                if b_rate > 0:
                    amt = (bill['amount'] / b_rate) * target_rate
                    trends_data[key] = trends_data.get(key, 0) + amt
        
        if hasattr(self, 'trends_chart'):
            self.trends_chart.set_data(trends_data)
        
        # Update Calendar
        if hasattr(self, 'calendar'):
            self.calendar.set_bills(self.unpaid_bills)

    def _on_tab_changed(self, index):
        """Handle tab changes for lazy loading."""
        # About tab is index 5 (0-indexed: Dashboard, Unpaid, Paid, Charts, Calendar, About)
        if index == 5:
            self._load_readme()


    def update_display(self):
        self.update_charts()
        # Update budget display
        curr = self.budget_currency_combo.currentText()
        rate = self.exchange_rates.get(curr, 1)
        if rate > 0:
            self.budget_input.setText(f"{self.budget * rate:,.2f}")
        
        # Update summary
        summary_curr = self.summary_currency_combo.currentText()
        summary_symbol = self.currencies.get(summary_curr, '$')
        summary_rate = self.exchange_rates.get(summary_curr, 1)
        
        if summary_rate > 0:
            total_usd = sum(b['amount'] / self.exchange_rates.get(b['currency'], 1) 
                          for b in self.unpaid_bills if self.exchange_rates.get(b['currency']))
            remaining_usd = self.budget - total_usd
            
            self.total_unpaid_label.setText(f"{STRINGS['total_unpaid_label']} {summary_symbol}{total_usd * summary_rate:,.2f}")
            self.remaining_budget_label.setText(f"{STRINGS['budget_after_paying_label']} {summary_symbol}{remaining_usd * summary_rate:,.2f}")
            
            if self.budget > 0:
                percentage = remaining_usd / self.budget
                self.progress_bar.setValue(max(0, int(percentage * 100)))
                if percentage < 0.25:
                    self.progress_bar.setStyleSheet("background-color: #f08080;")
                elif percentage < 0.50:
                    self.progress_bar.setStyleSheet("background-color: #ffa500;")
                else:
                    self.progress_bar.setStyleSheet("background-color: #90ee90;")
        
        # Update Unpaid Table
        self.unpaid_table.setRowCount(0)
        self.unpaid_table.setRowCount(len(self.unpaid_bills))
        
        for i, bill in enumerate(self.unpaid_bills):
            symbol = self.currencies.get(bill['currency'], '$')
            
            # Name
            name_item = QTableWidgetItem(bill['name'])
            # Amount
            amount_item = QTableWidgetItem(f"{symbol}{bill['amount']:,.2f}")
            # Category
            cat_item = QTableWidgetItem(bill.get('category', 'Other'))
            # Due Date
            due_date = bill.get('due_date', STRINGS["no_date_label"])
            date_item = QTableWidgetItem(due_date)
            # Frequency
            freq_item = QTableWidgetItem(bill.get('repeat_freq', 'No Repeat'))
            
            # Check overdue
            try:
                due = datetime.strptime(due_date, '%Y-%m-%d').date()
                if due < date.today():
                    for item in [name_item, amount_item, cat_item, date_item, freq_item]:
                        item.setForeground(QColor('#ff4d4d')) # Red text
            except:
                pass
                
            self.unpaid_table.setItem(i, 0, name_item)
            self.unpaid_table.setItem(i, 1, amount_item)
            self.unpaid_table.setItem(i, 2, cat_item)
            self.unpaid_table.setItem(i, 3, date_item)
            self.unpaid_table.setItem(i, 4, freq_item)
            
        # Update Paid Table (History)
        self.paid_table.setRowCount(0)
        self.paid_table.setRowCount(len(self.paid_bills))
        
        # Calculate Total Paid
        total_paid_usd = sum(b['amount'] / self.exchange_rates.get(b['currency'], 1) 
                            for b in self.paid_bills if self.exchange_rates.get(b['currency']))
        self.paid_summary_label.setText(f"Total Paid: {summary_symbol}{total_paid_usd * summary_rate:,.2f}")
        
        for i, bill in enumerate(self.paid_bills):
            symbol = self.currencies.get(bill['currency'], '$')
            
            self.paid_table.setItem(i, 0, QTableWidgetItem(bill['name']))
            self.paid_table.setItem(i, 1, QTableWidgetItem(f"{symbol}{bill['amount']:,.2f}"))
            self.paid_table.setItem(i, 2, QTableWidgetItem(bill.get('category', 'Other')))
            self.paid_table.setItem(i, 3, QTableWidgetItem(bill.get('due_date', '-'))) # Or paid date if we tracked it
            self.paid_table.setItem(i, 4, QTableWidgetItem(bill.get('repeat_freq', '-')))
    
    def show_unpaid_context_menu(self, position):
        """Show context menu for unpaid bills table."""
        idx = self.unpaid_table.indexAt(position)
        if not idx.isValid():
            return
            
        row = idx.row()
        if row < 0 or row >= len(self.unpaid_bills):
            return
            
        bill = self.unpaid_bills[row]
        
        menu = QMenu()
        pay_action = menu.addAction("💰 Pay Bill")
        edit_action = menu.addAction("✏️ Edit Bill")
        delete_action = menu.addAction("🗑️ Delete Bill")
        
        action = menu.exec(self.unpaid_table.viewport().mapToGlobal(position))
        
        if action == pay_action:
            self.pay_bill(bill)
        elif action == edit_action:
            self.edit_bill(bill)
        elif action == delete_action:
            self.delete_bill(bill)

    def show_paid_context_menu(self, position):
        """Show context menu for paid bills table."""
        idx = self.paid_table.indexAt(position)
        if not idx.isValid():
            return
            
        row = idx.row()
        if row < 0 or row >= len(self.paid_bills):
            return
            
        bill = self.paid_bills[row]
        
        menu = QMenu()
        restore_action = menu.addAction("↩️ Restore to Unpaid")
        delete_action = menu.addAction("🗑️ Delete Permanently")
        
        action = menu.exec(self.paid_table.viewport().mapToGlobal(position))
        
        if action == restore_action:
            self.paid_bills.pop(row)
            self.unpaid_bills.append(bill)
            self.save_data()
            self.update_display()
        elif action == delete_action:
            reply = QMessageBox.question(self, "Confirm Delete", 
                                       f"Are you sure you want to delete '{bill['name']}' from history?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.paid_bills.pop(row)
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
        self.unpaid_bills.sort(key=lambda b: datetime.strptime(b.get('due_date', '9999-12-31'), '%Y-%m-%d'))
        self.update_display()
    
    def sort_by_amount(self):
        self.unpaid_bills.sort(key=lambda b: b['amount'] / self.exchange_rates.get(b['currency'], 1), reverse=True)
        self.update_display()
    
    def open_converter(self):
        dialog = ConverterWindow(self, self.currencies, self.exchange_rates)
        dialog.exec()
    
    def open_settings(self):
        dialog = SettingsDialog(self, self.data_manager)
        dialog.exec()
    
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
    
    def closeEvent(self, event):
        """Handle window close event with user choice."""
        self.save_data()
        
        # If already marked for real close (from quit_app), just close
        if self.real_close:
            event.accept()
            return
        
        # Check if "Minimize to Tray" is enabled
        config = self.data_manager.load_config()
        minimize_to_tray = config.get('minimize_to_tray', True)
        
        if minimize_to_tray:
            # Ask user what they want to do
            reply = QMessageBox.question(
                self,
                'Close BillTracker',
                'What would you like to do?',
                QMessageBox.StandardButton.Close | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Cancel
            )
            
            # Add custom button text
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle('Close BillTracker')
            msg_box.setText('What would you like to do?')
            msg_box.setIcon(QMessageBox.Icon.Question)
            
            minimize_btn = msg_box.addButton('Minimize to Tray', QMessageBox.ButtonRole.AcceptRole)
            quit_btn = msg_box.addButton('Quit Application', QMessageBox.ButtonRole.RejectRole)
            msg_box.addButton(QMessageBox.StandardButton.Cancel)
            
            msg_box.exec()
            clicked = msg_box.clickedButton()
            
            if clicked == minimize_btn:
                # Minimize to tray
                event.ignore()
                self.hide()
                self.tray_icon.showMessage(
                    "BillTracker",
                    "App is running in the background.",
                    QSystemTrayIcon.MessageIcon.Information,
                    2000
                )
            elif clicked == quit_btn:
                # Quit application
                self.real_close = True
                self.tray_icon.hide()
                event.accept()
                QApplication.quit()
            else:
                # Cancel
                event.ignore()
        else:
            # Minimize to tray disabled, just close
            event.accept()

    def quit_app(self):
        """Properly quit the application."""
        self.real_close = True
        self.tray_icon.hide()  # Hide tray icon before quitting
        QApplication.quit()  # Properly quit the application

    def show_window(self):
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowState.WindowMinimized | Qt.WindowState.WindowActive)
        self.activateWindow()

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.show_window()


    
    def export_csv(self):
        """Export data to CSV."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Export CSV", "", "CSV Files (*.csv)")
        if not file_path:
            return
            
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Name', 'Amount', 'Currency', 'Category', 'Frequency', 'Due Date', 'Status'])
                for b in self.unpaid_bills:
                    writer.writerow([b['name'], b['amount'], b['currency'], b.get('category', 'Other'), b.get('repeat_freq', 'No Repeat'), b.get('due_date', ''), 'Unpaid'])
                for b in self.paid_bills:
                    writer.writerow([b['name'], b['amount'], b['currency'], b.get('category', 'Other'), b.get('repeat_freq', 'No Repeat'), b.get('due_date', ''), 'Paid'])
            QMessageBox.information(self, "Export Successful", f"Data exported to {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", str(e))

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()
        
        # Save preference
        config = self.data_manager.load_config()
        config['dark_mode'] = self.is_dark_mode
        self.data_manager.save_config(config)

    def apply_theme(self):
        app = QApplication.instance()
        if self.is_dark_mode:
            # Modern Dark Theme QSS
            qss = """
            QMainWindow, QDialog {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QWidget {
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                color: #eeeeee;
            }
            QLabel {
                color: #eeeeee;
            }
            QLineEdit, QComboBox, QDateEdit, QSpinBox, QDoubleSpinBox {
                background-color: #2d2d2d;
                border: 1px solid #3e3e3e;
                border-radius: 4px;
                padding: 4px;
                color: #ffffff;
                selection-background-color: #3a86ff;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 1px solid #3a86ff;
            }
            QPushButton {
                background-color: #3a86ff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2a76ef;
            }
            QPushButton:pressed {
                background-color: #1a66df;
            }
            QListWidget, QTableWidget {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3e3e3e;
                border-radius: 4px;
                outline: none;
            }
            QListWidget::item, QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #3e3e3e;
            }
            QListWidget::item:selected, QTableWidget::item:selected {
                background-color: #3a86ff;
                color: white;
            }
            QHeaderView::section {
                background-color: #1e1e1e;
                color: #aaaaaa;
                padding: 5px;
                border: 1px solid #3e3e3e;
            }
            QGroupBox {
                border: 1px solid #3e3e3e;
                border-radius: 6px;
                margin-top: 1.5em; /* leave space for the title */
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left; 
                padding: 0 5px;
                color: #3a86ff;
            }
            QProgressBar {
                border: 1px solid #3e3e3e;
                border-radius: 4px;
                text-align: center;
                background-color: #2d2d2d;
            }
            QProgressBar::chunk {
                background-color: #3a86ff;
                border-radius: 3px;
            }
            QTabWidget::pane {
                border: 1px solid #3e3e3e;
                background-color: #1e1e1e;
            }
            QTabBar::tab {
                background-color: #2d2d2d;
                color: #aaaaaa;
                padding: 8px 16px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #3a86ff;
                color: white;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #2d2d2d;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #555555;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            } 
            """
            app.setStyle("Fusion")
            app.setStyleSheet(qss)
        else:
            # Light Theme (Clean White & Black)
            qss = """
            QMainWindow, QDialog {
                background-color: #ffffff;
                color: #000000;
            }
            QWidget {
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                color: #000000;
            }
            QLabel {
                color: #000000;
            }
            QLineEdit, QComboBox, QDateEdit, QSpinBox, QDoubleSpinBox {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 4px;
                color: #000000;
                selection-background-color: #007bff;
                selection-color: #ffffff;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 1px solid #007bff;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0069d9;
            }
            QPushButton:pressed {
                background-color: #0056b3;
            }
            QListWidget, QTableWidget {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 4px;
                color: #000000;
                outline: none;
                gridline-color: #eeeeee;
            }
            QListWidget::item, QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eeeeee;
                color: #000000;
            }
            QListWidget::item:selected, QTableWidget::item:selected {
                background-color: #e8f0fe;
                color: #1967d2;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                color: #000000;
                padding: 5px;
                border: 1px solid #cccccc;
            }
            QGroupBox {
                border: 1px solid #dddddd;
                border-radius: 6px;
                margin-top: 1.5em;
                font-weight: bold;
                background-color: #ffffff;
                color: #000000;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                color: #007bff;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background-color: #ffffff;
            }
            QTabBar::tab {
                background-color: #f0f0f0;
                color: #000000;
                padding: 8px 16px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #007bff;
                color: white;
            }
            """
            app.setStyle("Fusion")
            app.setStyleSheet(qss)

if __name__ == "__main__":
    # Taskbar icon fix
    myappid = 'grouvya.billtracker.qt.5.3.0'
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path('calc.ico')))
    
    # Show splash screen
    splash = SplashScreen()
    splash.show()
    app.processEvents()
    
    # Simulate initialization with progress updates
    splash.update_progress(10, "Loading configuration...")
    QTimer.singleShot(100, lambda: None)  # Small delay for visual effect
    app.processEvents()
    
    splash.update_progress(30, "Initializing security...")
    QTimer.singleShot(100, lambda: None)
    app.processEvents()
    
    splash.update_progress(50, "Loading exchange rates...")
    QTimer.singleShot(100, lambda: None)
    app.processEvents()
    
    splash.update_progress(70, "Preparing interface...")
    window = BillTrackerWindow()
    app.processEvents()
    
    splash.update_progress(90, "Finalizing...")
    QTimer.singleShot(100, lambda: None)
    app.processEvents()
    
    splash.update_progress(100, "Ready!")
    
    # Close splash and show main window
    QTimer.singleShot(500, splash.close)
    QTimer.singleShot(600, window.show)
    
    sys.exit(app.exec())

