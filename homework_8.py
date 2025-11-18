import flet as ft
from datetime import datetime

def main(page: ft.Page):
    page.title = "Daily Expenses"
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    categories = ["Food", "Transportation", "Entertainment", "Utilities"]
    expenses = []

    category_dd = ft.Dropdown(
        label="Category",
        options=[ft.dropdown.Option(c) for c in categories],
        width=200
    )

    amount_tf = ft.TextField(
        label="Amount",
        width=150,
        keyboard_type=ft.KeyboardType.NUMBER
    )

    desc_tf = ft.TextField(
        label="Description",
        width=350
    )

    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Date")),
            ft.DataColumn(ft.Text("Category")),
            ft.DataColumn(ft.Text("Amount")),
            ft.DataColumn(ft.Text("Description")),
        ],
        rows=[],
    )

    table_section = ft.Container(
        content=ft.Column(
            [data_table],
            scroll=ft.ScrollMode.AUTO
        ),
        height=300,
        border=ft.border.all(1, ft.Colors.GREY_400),
        padding=10,
    )

    pie_chart = ft.PieChart(
        sections=[],
        sections_space=2,
        center_space_radius=65,
        height=260,
        width=260
    )

    def update_chart():
        # totals for pie chart
        totals = {cat: 0 for cat in categories}
        for exp in expenses:
            totals[exp["category"]] += exp["amount"]

        # pie chart sections
        colors = [
            ft.Colors.BLUE,
            ft.Colors.GREEN,
            ft.Colors.ORANGE,
            ft.Colors.RED,
        ]

        sections = []
        grand_total = sum(totals.values())

        for i, (cat, amount) in enumerate(totals.items()):
            if amount > 0:
                pct = (amount / grand_total) * 100 if grand_total > 0 else 0
                sections.append(
                    ft.PieChartSection(
                        value=amount,
                        color=colors[i % len(colors)],
                        radius=80,
                        title=f"{pct:.1f}%",
                        title_style=ft.TextStyle(
                            color=ft.Colors.WHITE,
                            size=12,
                            weight=ft.FontWeight.BOLD,
                        ),
                    )
                )

        pie_chart.sections = sections
        pie_chart.update()

    def add_expense(e):
        if not category_dd.value:
            category_dd.error_text = "Choose a category"
            category_dd.update()
            return
        
        if not amount_tf.value or float(amount_tf.value) <= 0:
            amount_tf.error_text = "Enter valid amount"
            amount_tf.update()
            return

        # clear errors
        category_dd.error_text = None
        amount_tf.error_text = None

        # create expense entry
        expense = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "category": category_dd.value,
            "amount": float(amount_tf.value),
            "description": desc_tf.value or "",
        }

        expenses.append(expense)

        # add a row to table when a new expense is added
        data_table.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(expense["date"])),
                    ft.DataCell(ft.Text(expense["category"])),
                    ft.DataCell(ft.Text(f"${expense['amount']:.2f}")),
                    ft.DataCell(ft.Text(expense["description"])),
                ]
            )
        )
        data_table.update()
        update_chart()

        # clear fields
        category_dd.value = None
        amount_tf.value = ""
        desc_tf.value = ""
        page.update()

        page.snack_bar = ft.SnackBar(
            content=ft.Text("Expense added!"),
            open=True,
        )
        page.update()

    add_btn = ft.ElevatedButton(
        "Add Expense",
        icon=ft.Icons.ADD,
        on_click=add_expense,
    )

    # page layout
    page.add(
        ft.Text("Add Expense", size=22, weight=ft.FontWeight.BOLD),
        ft.Row([category_dd, amount_tf]),
        desc_tf,
        add_btn,
        ft.Divider(height=30),
        ft.Text("Expense Distribution", size=22, weight=ft.FontWeight.BOLD),
        pie_chart,
        ft.Divider(height=30),
        ft.Text("Expense History", size=22, weight=ft.FontWeight.BOLD),
        table_section,
    )

if __name__ == "__main__":
    ft.app(target=main)
