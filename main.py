# marketing_campaigns.csv

import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import csv


class CampaignAnalyzer:
    def load(self):
        try:
            with open("marketing_campaigns.csv", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                table = Table(title="📊 Campaign Data", show_lines=True)

                # Define table columns with styling
                table.add_column("Campaign_ID", justify="right", style="purple")
                table.add_column("Campaign_Name", justify="right", style="bold magenta")
                table.add_column("Start_Date", justify="right", style="yellow")
                table.add_column("Impressions", justify="right", style="bold green")
                table.add_column("Clicks", justify="right", style="green")
                table.add_column(
                    "Conversions", justify="right", style=" Cyan"
                )  # Fixed `orange`
                table.add_column("Cost ($)", justify="right", style="red")
                table.add_column("Revenue ($)", justify="right", style="bold white")

                next(reader)  # Skip the header row

                for row in reader:
                    try:
                        table.add_row(
                            row[0],  # Campaign_ID
                            row[1],  # Campaign_Name
                            row[2],  # Start_Date (Ensure this matches the CSV header)
                            f"{int(row[3]):,}",  # Impressions (Formatted with ,)
                            f"{int(row[4]):,}",  # Clicks (Formatted with ,)
                            f"{int(row[5]):,}",  # Conversions (Formatted with ,)
                            f"${float(row[6]):,.2f}",  # Cost (Formatted as currency)
                            f"${float(row[7]):,.2f}",  # Revenue (Formatted as currency)
                        )
                    except ValueError:
                        continue  # Skip rows with invalid data

                console = Console()
                console.print(table)

        except FileNotFoundError:
            print(" Error: 'marketing_campaigns.csv' not found!")
        except Exception as e:
            print(f" Unexpected Error: {e}")

    def total_revenue(self):
        try:
            df = pd.read_csv("marketing_campaigns.csv")
            table = Table(title="📊 Campaigns Revenue", show_lines=True)

            # Define table columns with styling
            table.add_column("Campaign_ID", justify="right", style="purple")
            table.add_column("Campaign_Name", justify="right", style="bold magenta")
            table.add_column("Start_Date", justify="right", style="Cyan")
            table.add_column("Real_Revenue ($)", justify="right", style="bold green")
            df["real_revenue"] = df["Revenue"] - df["Cost"]
            df = df.sort_values(by="real_revenue", ascending=False)

            for index, row in df.iterrows():
                table.add_row(
                    str(row["Campaign_ID"]),
                    row["Campaign_Name"],
                    row["Start_Date"],
                    f"${row['real_revenue']:,.2f}",  # Form
                )

            console = Console()
            console.print(table)

        except FileNotFoundError:
            print("Error: 'marketing_campaigns.csv' not found!")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def conversion_rate(self):
        try:
            df = pd.read_csv("marketing_campaigns.csv")

            table = Table(title="conversion rate", show_lines=True)
            table.add_column("Campaign_ID", justify="right", style="purple")
            table.add_column("Campaign_Name", justify="right", style="Cyan")
            table.add_column("Start_Date", justify="right", style="bold magenta")
            table.add_column("Conversion rate", justify="right", style="bold green")

            df["conversion rate"] = df["Conversions"] / df["Clicks"]
            df = df.sort_values(by="conversion rate", ascending=False)

            for index, row in df.iterrows():
                table.add_row(
                    str(row["Campaign_ID"]),
                    row["Campaign_Name"],
                    row["Start_Date"],
                    f"{row['conversion rate']:.2%}",
                )

            console = Console()
            console.print(table)
        except FileNotFoundError:
            print("Error: 'marketing_campaigns.csv' not found!")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def CTR(self):
        console = Console()

        table = Table(title="CTR", show_lines=True)
        table.add_column("Campaign_ID", justify="right", style="purple")
        table.add_column("Campaign_Name", justify="right", style="Cyan")
        table.add_column("Start_Date", justify="right", style="bold magenta")
        table.add_column("CTR", justify="right", style="bold green")

        df = pd.read_csv("marketing_campaigns.csv")
        df["CTR_value"] = df["Clicks"] / df["Impressions"] * 100
        df = df.sort_values(by="CTR_value", ascending=False)

        for index, row in df.iterrows():
            table.add_row(
                str(row["Campaign_ID"]),
                row["Campaign_Name"],
                row["Start_Date"],
                f"{row['CTR_value']:.2f}%",
            )
        console.print(table)

    def Cost_per_click(self):
        console = Console()

        table = Table(title="Cost per click", show_lines=True)
        table.add_column("Campaign_ID", justify="right", style="purple")
        table.add_column("Campaign_Name", justify="right", style="Cyan")
        table.add_column("Start_Date", justify="right", style="bold magenta")
        table.add_column("Cost per click", justify="right", style="bold green")

        df = pd.read_csv("marketing_campaigns.csv")
        df["CPC"] = df["Cost"] / df["Clicks"]
        df = df.sort_values(by="CPC", ascending=False)

        for index, row in df.iterrows():
            table.add_row(
                str(row["Campaign_ID"]),
                row["Campaign_Name"],
                row["Start_Date"],
                f"${row['CPC']:,.2f}",
            )
        console.print(table)
        console.print(
            "[bold white]Lower CPC → More efficient spending \nHigher CPC → Might indicate high competition or poor ad targeting   [/bold white]"
        )

    def insights(self):
        data = analysis.compile_Data()
        console = Console()

        metrics = ["CTR (%)", "CPC", "Conversion Rate (%)", "Real Revenue"]

        for campaign in data:
            try:
                campaign_id = campaign.get("Campaign_ID", "N/A")
                campaign_name = campaign.get("Campaign_Name", "N/A")
                Start_date = campaign.get("Start_Date", "N/A")
                impressions = int(campaign.get("Impressions", 0))
                clicks = int(campaign.get("Clicks", 0))
                conversions = int(campaign.get("Conversions", 0))
                cost = float(campaign.get("Cost", 0))
                revenue = float(campaign.get("Revenue", 0))

                ctr = (clicks / impressions * 100) if impressions > 0 else 0
                cpc = (cost / clicks) if clicks > 0 else 0
                conversion_rate = (conversions / clicks * 100) if clicks > 0 else 0
                real_revenue = revenue - cost

                table = Table(
                    title=f"Campaign Metrics Overview for {campaign_name} ID: {campaign_id} Start Date: {Start_date}",
                    show_lines=True,
                )
                table.add_column("Metric", justify="right", style="bold magenta")
                table.add_column("Value", justify="right", style="bold green")

                values = [ctr, cpc, conversion_rate, real_revenue]

                for metric, value in zip(metrics, values):
                    table.add_row(metric, f"{value:,.2f}")

                console.print(table)

            except ValueError:
                continue  # Skip rows with invalid data

    def search_insights(self):
        console = Console()
        df = pd.read_csv("marketing_campaigns.csv")

        # Display all campaign names
        campaign_names = df["Campaign_Name"].unique()
        console.print("[bold cyan]Available Campaigns:[/bold cyan]")
        for name in campaign_names:
            console.print(f"- {name}")

        # Prompt user to search for a campaign
        search_name = input("Enter the campaign name to view insights: ").strip()

        # Filter the dataframe for the selected campaign
        campaign_data = df[
            df["Campaign_Name"].str.contains(search_name, case=False, na=False)
        ]

        if not campaign_data.empty:
            for index, row in campaign_data.iterrows():
                campaign_id = row["Campaign_ID"]
                campaign_name = row["Campaign_Name"]
                start_date = row["Start_Date"]
                impressions = int(row["Impressions"])
                clicks = int(row["Clicks"])
                conversions = int(row["Conversions"])
                cost = float(row["Cost"])
                revenue = float(row["Revenue"])

                ctr = (clicks / impressions * 100) if impressions > 0 else 0
                cpc = (cost / clicks) if clicks > 0 else 0
                conversion_rate = (conversions / clicks * 100) if clicks > 0 else 0
                real_revenue = revenue - cost

                table = Table(
                    title=f"Campaign Metrics Overview for {campaign_name} ID: {campaign_id} Start Date: {start_date}",
                    show_lines=True,
                )
                table.add_column("Metric", justify="right", style="bold magenta")
                table.add_column("Value", justify="right", style="bold green")

                metrics = ["CTR (%)", "CPC", "Conversion Rate (%)", "Real Revenue"]
                values = [ctr, cpc, conversion_rate, real_revenue]

                for metric, value in zip(metrics, values):
                    table.add_row(metric, f"{value:,.2f}")

                console.print(table)
        else:
            console.print("[bold red]No campaign found with that name.[/bold red]")

    def main_menu(self):
        try:
            menu_text = """
             [bold cyan] Marketing Campagin Analysis[/bold cyan]
             [bold white]1.[/bold white] Show campagin data
             [bold white]2.[/bold white] Total Revenue
             [bold white]3.[/bold white] Conversion Rate
             [bold white]4.[/bold white] Click Through Rate
             [bold white]5.[/bold white] Cost per click
             [bold white]6.[/bold white] Wholesome insights
             [bold white]7.[/bold white] search insights
             [bold white]0.[/bold white] Exit

             """
            console = Console()
            console.print(
                Panel(
                    menu_text,
                    title="[bold yellow] Menu [/bold yellow]",
                    border_style="Purple",
                )
            )

        except FileNotFoundError:
            print("Error: 'marketing_campaigns.csv' not found!")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def compile_Data(file_path="marketing_campaigns.csv"):
        with open("marketing_campaigns.csv", "r") as file:
            reader = csv.DictReader(file)
            return list(reader)

    def choices(self):
        console = Console()
        analysis.compile_Data()

        while True:
            analysis.main_menu()
            choice = input("Enter choice: ").strip()
            if choice == "1":
                analysis.load()
            elif choice == "2":
                analysis.total_revenue()
            elif choice == "3":
                analysis.conversion_rate()
            elif choice == "4":
                analysis.CTR()
            elif choice == "5":
                analysis.Cost_per_click()
            elif choice == "6":
                analysis.insights()
            elif choice == "7":
                analysis.search_insights()
            elif choice == "0":
                console.print("[bold cyan]Goodbye![/bold cyan]")
                break

            else:
                console.print("[bold red]Invalid choice. Please try again.[/bold red]")


analysis = CampaignAnalyzer()

analysis.choices()
