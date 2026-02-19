
import re

# Paste the current content of get_currency_list here or import it if possible.
# Since I can't easily import a specific function from a large file without running it (and it has deps), 
# I'll just parse the dictionary from the file content I specifically read.

def extract_symbols():
    # This dictionary is copied from the view_code_item output of get_currency_list
    current_list = {
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
        'ر (QAR)': 'ر.ق', '﷼ (IRR)': '﷼', 'D (GMD)': 'D', 'Le (SLL)': 'Le', '₾ (GEL)': '₾'
    }
    
    symbol_map = {}
    for key in current_list:
        # Key format is "Symbol (Code)"
        match = re.search(r'\((.*?)\)$', key)
        if match:
            code = match.group(1)
            symbol = current_list[key]
            symbol_map[code] = symbol
            

    with open('symbols_out.txt', 'w', encoding='utf-8') as f:
        f.write("CURRENCY_SYMBOLS = {\n")
        sorted_codes = sorted(symbol_map.keys())
        for i, code in enumerate(sorted_codes):
            comma = "," if i < len(sorted_codes) - 1 else ""
            f.write(f"    '{code}': '{symbol_map[code]}'{comma}\n")
        f.write("}\n")


if __name__ == "__main__":
    extract_symbols()
