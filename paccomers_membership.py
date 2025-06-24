"""
PacCommers ingin memprediksi tier membership (Platinum, Gold, Silver) untuk user berdasarkan:

Monthly expense (pengeluaran bulanan)

Monthly income (pendapatan bulanan)

Metode yang digunakan adalah Euclidean Distance untuk menghitung jarak antara data user dengan parameter masing-masing membership.

"""

import math
from tabulate import tabulate

"""
pakai tabulate untuk menampilkan tabel

class PacCommersMembership memiliki atribut:
username (string)
monthly_expense (integer)
monthly_income (integer)
membership (string)
membership_params (dictionary)
membership_benefits (dictionary)

method:
show_benefits() : menampilkan benefit semua membership

predict_membership() : memprediksi membership berdasarkan expense dan income user
Rumus: √((expense_user - expense_membership)² + (income_user - income_membership)²)
Memilih membership dengan jarak terdekat

calculate_price() : menghitung total harga setelah diskon berdasarkan membership
"""



import math
from tabulate import tabulate

class PacCommersMember:
    def __init__(self, username, monthly_expense, monthly_income):
        self.username = username
        self.monthly_expense = monthly_expense
        self.monthly_income = monthly_income
        self.membership = None
        
        # Parameter membership (expense, income)
        self.membership_params = {
            'platinum': (8, 15),
            'gold': (6, 10),
            'silver': (5, 7)
        }
        
        # Benefit masing-masing membership
        self.membership_benefits = {
            'platinum': {
                'discount': '15%',
                'benefits': [
                    'Benefit silver + gold',
                    'Voucher liburan',
                    'Cashback max. 30%'
                ]
            },
            'gold': {
                'discount': '10%',
                'benefits': [
                    'Benefit silver',
                    'Voucher ojek online'
                ]
            },
            'silver': {
                'discount': '8%',
                'benefits': [
                    'Voucher makanan'
                ]
            }
        }
    
    def show_benefits(self):
        """Menampilkan benefit semua membership dalam tabel rapi"""
        headers = ["Tier", "Discount", "Benefits"]
        table_data = []
        
        for tier, details in self.membership_benefits.items():
            benefits = "\n".join(details['benefits'])
            table_data.append([
                tier.upper(),
                details['discount'],
                benefits
            ])
        
        print("\n=== DAFTAR BENEFIT MEMBERSHIP ===")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    def show_requirements(self):
        """Menampilkan syarat membership dalam tabel"""
        headers = ["Tier", "Monthly Expense (juta)", "Monthly Income (juta)"]
        table_data = []
        
        for tier, params in self.membership_params.items():
            table_data.append([
                tier.upper(),
                params[0],
                params[1]
            ])
        
        print("\n=== SYARAT MEMBERSHIP ===")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    def predict_membership(self):
        """
        Memprediksi membership berdasarkan Euclidean Distance.
        Rumus: √((expense_user - expense_membership)² + (income_user - income_membership)²)
        """
        distances = {}
        
        for tier, params in self.membership_params.items():
            expense_diff = self.monthly_expense - params[0]
            income_diff = self.monthly_income - params[1]
            distances[tier] = math.sqrt(expense_diff**2 + income_diff**2)
        
        # Gunakan lambda untuk mendapatkan tier dengan jarak terkecil
        self.membership = min(distances.keys(), key=lambda k: distances[k])
        
        # data untuk tabel
        headers = ["Tier", "Jarak Euclidean"]
        table_data = [[tier.upper(), f"{dist:.2f}"] for tier, dist in distances.items()]
        
        print("\n=== HASIL PREDIKSI ===")
        print(f"User: {self.username}")
        print(f"Expense: {self.monthly_expense} juta | Income: {self.monthly_income} juta\n")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print(f"\n✨ Predicted Membership: {self.membership.upper()} ✨")
        
        return self.membership
    
    def calculate_price(self, items_price):
        """Menghitung total harga setelah diskon"""
        if not self.membership:
            print("Prediksi membership terlebih dahulu!")
            return None
        
        total_price = sum(items_price)
        
        # Hitung diskon
        discount_rates = {'platinum': 0.15, 'gold': 0.10, 'silver': 0.08}
        discount = discount_rates.get(self.membership, 0)
        final_price = total_price * (1 - discount)
        
        # Tampilkan dalam tabel
        headers = ["Description", "Amount"]
        table_data = [
            ["Total Harga", f"Rp {total_price:,}"],
            ["Membership", self.membership.upper()],
            ["Discount", f"{discount*100}%"],
            ["Harga Final", f"Rp {final_price:,.2f}"]
        ]
        
        print("\n=== TOTAL PEMBAYARAN ===")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        return final_price


if __name__ == "__main__":
    # Contoh penggunaan
    user = PacCommersMember("Kresna", 7, 12)
    
    # Tampilkan benefit dan syarat
    user.show_benefits()
    user.show_requirements()
    
    # Prediksi membership
    user.predict_membership()
    
    # Hitung total belanja
    items = [500000, 750000, 1200000]  # Contoh harga barang
    user.calculate_price(items)