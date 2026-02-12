# 💰 BillTracker - The Premium Financial Hub

**Version 7.1.12** | Created with ❤️ by **Grouvya**

A modern, high-performance financial management ecosystem. Streamline your bills, automate your subscriptions, and crush your savings goals—all from a single, secure, and beautiful interface.

---

## Compiling on Linux Mint / Ubuntu

If you are on Linux Mint or Ubuntu, you can use the specialized compilation script provided:

1.  Open a terminal in the project directory.
2.  Make the script executable:
    ```bash
    chmod +x mint_compile.sh
    ```
3.  Run the script:
    ```bash
    ./mint_compile.sh
    ```

The script will automatically install system dependencies, set up a virtual environment, and build the executable in the `dist` folder.

---

## 💎 Core Experience

### 📊 The Financial Command Center
- **Unified 360° Dashboard**: Instant clarity on your budget, upcoming bills, and savings milestones.
- **Smart Subscription Engine**: Identify "burn rate" patterns and manage recurring costs with surgical precision.
- **Savings Ecosystem**: Set targets, visualize progress with interactive charts, and reach your goals faster.
- **Advanced Global Search**: Lightning-fast (Ctrl+F) engine to find any transaction across categories, dates, or amounts.

### 🛡️ Iron-Clad Security
- **AES-256 Military-Grade Encryption**: Your data is protected by the industry standard (Fernet architecture).
- **Secure PIN Access**: 4-6 digit biometric-inspired protection with brute-force lockout.
- **Auto-Lock Intelligence**: Customizable idle timeouts and "lock-on-minimize" to keep your data private in any environment.
- **Atomic Data Integrity**: Fail-safe save mechanisms and SHA-256 checksum verification protect against corruption.

---

## 🚀 Milestone History (v7.1.12)

### v7.1.12 - "Final Stability Hotfix"
- **Comprehensive Audit**: Resolved all potential `NoneType` parent access issues across `PinEntryDialog`, `SettingsDialog`, and `ToastNotification`.
- **System Robustness**: Standardized theme manager resolution to ensure the app remains functional even during complex startup sequences or background tasks.

### v7.1.11 - "Startup Security Hotfix"
- **Hotfix**: Resolved a critical crash at launch when PIN security was active.

### v7.1.10 - "Pin & Theme Stability"
- **Hotfix**: Fixed `AttributeError` when modifying PIN settings.

---

## 📧 Support & Community

Dedicated to providing the best personal finance tool. For feedback, feature requests, or support, use the **📩 Contact** button inside the app's About tab.

**Thank you for choosing BillTracker!** 🎉
