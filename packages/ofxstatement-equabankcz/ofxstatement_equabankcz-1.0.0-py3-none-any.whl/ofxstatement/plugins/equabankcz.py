import csv
from datetime import datetime
from typing import Iterable, Optional, List

from ofxstatement import statement
from ofxstatement.statement import StatementLine
from ofxstatement.plugin import Plugin
from ofxstatement.parser import CsvStatementParser


class EquaBankParser(CsvStatementParser):
    date_format = "%d.%m.%Y"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, *kwargs)
        self.columns = None
        self.mappings = {}

    def split_records(self) -> Iterable[str]:
        """
        Return iterable object consisting of a line per transaction
        """
        return csv.reader(self.fin, delimiter=";", quotechar='"')

    def parse_record(self, line: List[str]) -> Optional[StatementLine]:
        """Parse given transaction line and return StatementLine object"""

        # First line of CSV file contains headers, not an actual transaction
        if self.cur_record == 1:
            # Prepare columns headers lookup table for parsing
            self.columns = {v: i for i, v in enumerate(line)}
            self.mappings = {
                "date": self.columns["Datum vystavení"],
                "memo": self.columns["Místo transakce"],
                "payee": self.columns["Název účtu protistrany"],
                "amount": self.columns["Částka"],
                "check_no": self.columns["Variabilní symbol"],
                "refnum": self.columns["Kód transakce"],
            }
            # And skip further processing by parser
            return None

        # Shortcut
        columns = self.columns

        # Normalize string
        for i, v in enumerate(line):
            line[i] = v.strip()

        if line[columns["Částka"]] == "":
            line[columns["Částka"]] = "0"

        statement_line = super().parse_record(line)

        # Ignore lines, which do not have posting date yet (typically pmts by debit cards
        # have some delays).
        if line[columns["Datum vystavení"]]:
            statement_line.date_user = line[columns["Datum vystavení"]]
            statement_line.date_user = datetime.strptime(
                statement_line.date_user, self.date_format
            )

        statement_line.id = statement.generate_transaction_id(statement_line)

        # Manually set some of the known transaction types
        payment_type = line[columns["Typ pohybu"]]
        if payment_type.startswith("Srážková daň z úroků"):
            statement_line.trntype = "DEBIT"
        elif payment_type.startswith("Připsaný úrok"):
            statement_line.trntype = "INT"
        elif payment_type.startswith("Poplatky"):
            statement_line.trntype = "FEE"
        elif payment_type.startswith("Okamžitá domácí platba"):
            statement_line.trntype = "XFER"
        elif payment_type.startswith("Příchozí"):
            statement_line.trntype = "XFER"
        elif payment_type.startswith("Vrácení platby"):
            statement_line.trntype = "XFER"
        elif payment_type.startswith("Odchozí"):
            statement_line.trntype = "XFER"
        elif payment_type.startswith("Platba v rámci"):
            statement_line.trntype = "XFER"
        elif payment_type.startswith("Výběr hotovosti"):
            statement_line.trntype = "ATM"
        elif payment_type.startswith("Platba kartou"):
            statement_line.trntype = "POS"
        elif payment_type.startswith("Inkaso"):
            statement_line.trntype = "DIRECTDEBIT"
        elif payment_type.startswith("Trvalý"):
            statement_line.trntype = "REPEATPMT"
        else:
            print(
                'WARN: Unexpected type of payment appeared - "{}". Using XFER transaction type instead'.format(
                    payment_type
                )
            )
            statement_line.trntype = "XFER"

        # .payee becomes OFX.NAME which becomes "Description" in GnuCash
        # .memo  becomes OFX.MEMO which becomes "Notes"       in GnuCash
        # When .payee is empty, GnuCash imports .memo to "Description" and keeps "Notes" empty

        # throw out generic card payment names and associated account numbers
        if line[columns["Název účtu protistrany"]].startswith("NOSTRO") or line[
            columns["Název účtu protistrany"]
        ].startswith("SUSPENSE"):
            statement_line.payee = ""
        # statement_line.payee = "Název účtu protistrany" + "Číslo účtu protistrany"
        elif line[columns["Číslo účtu protistrany"]] != "":
            statement_line.payee += "|ÚČ: " + line[columns["Číslo účtu protistrany"]]

        # statement_line.memo = "Popis pohybu" + the payment identifiers
        if line[columns["Popis pohybu"]] != "":
            # if Popis pohybu is present, it means that place is not relevant
            # because card payments do not have this property
            statement_line.memo = line[columns["Popis pohybu"]]
        if not self.empty_or_null(line[columns["Variabilní symbol"]]):
            statement_line.memo += "|VS: " + line[columns["Variabilní symbol"]]

        if not self.empty_or_null(line[columns["Konstantní symbol"]]):
            statement_line.memo += "|KS: " + line[columns["Konstantní symbol"]]

        if not self.empty_or_null(line[columns["Specifický symbol"]]):
            statement_line.memo += "|SS: " + line[columns["Specifický symbol"]]

        # throw out memo if it would be the same as payee
        if statement_line.payee == "" and statement_line.memo:
            statement_line.payee = statement_line.memo
            statement_line.memo = ""

        if statement_line.amount == 0:
            return None

        return statement_line

    @staticmethod
    def empty_or_null(value: str) -> bool:
        return value in ["", "0"]


class EquaBankCZPlugin(Plugin):
    """Equa Bank a.s. (Czech Republic) (CSV, UTF-8)"""

    def get_parser(self, filename: str) -> EquaBankParser:
        EquaBankCZPlugin.encoding = self.settings.get("charset", "utf-8")
        file = open(filename, "r", encoding=EquaBankCZPlugin.encoding)
        parser = EquaBankParser(file)
        parser.statement.currency = self.settings.get("currency", "CZK")
        parser.statement.bank_id = self.settings.get("bank", "EQBKCZPP")
        parser.statement.account_id = self.settings.get("account", "")
        parser.statement.account_type = self.settings.get("account_type", "CHECKING")
        parser.statement.trntype = "OTHER"
        return parser
