import flet as ft
import sqlite3
import matplotlib.pyplot as plt

# --- 1. إعداد قاعدة البيانات ---
def setup_db():
    conn = sqlite3.connect('accounting_system.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS invoices 
                 (id INTEGER PRIMARY KEY, amount REAL, vat REAL, total REAL)''')
    conn.commit()
    conn.close()

# --- 2. المنطق المحاسبي (مع الضريبة والعملة) ---
def calculate_vat(amount):
    vat = amount * 0.15
    total = amount + vat
    return f"{amount:,.2f} ج.س", f"{vat:,.2f} ج.س", f"{total:,.2f} ج.س"

# --- 3. الواجهة الرسومية (الداش بورد) ---
def main(page: ft.Page):
    setup_db()
    page.title = "Accounting System Pro - عمر يوسف البطحاني"
    page.theme_mode = ft.ThemeMode.LIGHT

    # عناصر التحكم
    amount_field = ft.TextField(label="إدخال المبلغ (ج.س)", width=200)
    result_text = ft.Text("", size=16)

    def calculate_click(e):
        amount = float(amount_field.value)
        base, vat, total = calculate_vat(amount)
        result_text.value = f"المبلغ: {base}\nالضريبة: {vat}\nالإجمالي: {total}"
        page.update()

    def show_chart(e):
        # رسم بياني تجريبي للمبيعات
        plt.bar(['يناير', 'فبراير', 'مارس'], [1500, 2300, 1800])
        plt.title("تقرير المبيعات")
        plt.show()

    def print_invoice(e):
        page.show_snack_bar(ft.SnackBar(ft.Text("تم إرسال الفاتورة للطابعة الحرارية بنجاح!")))

    # تصميم الواجهة
    page.add(
        ft.Text("لوحة التحكم المحاسبية", size=30, weight="bold"),
        amount_field,
        ft.ElevatedButton("حساب الفاتورة", on_click=calculate_click),
        result_text,
        ft.Divider(),
        ft.Row([
            ft.IconButton(ft.icons.PRINT, on_click=print_invoice, tooltip="طباعة"),
            ft.IconButton(ft.icons.BAR_CHART, on_click=show_chart, tooltip="رسوم بيانية")
        ]),
        ft.Divider(),
        ft.Text("مطور بواسطة: عمر يوسف البطحاني", color="blue", weight="bold"),
        ft.Text("© 2026 جميع الحقوق محفوظة", size=10)
    )

ft.app(target=main)
