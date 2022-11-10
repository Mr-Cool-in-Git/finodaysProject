from typing import List, Optional
from fastapi import Depends, HTTPException, status

from ..database import Session, get_session
from ..models.user import User
from .. import tables
import hashlib

import pandas as pd
import requests
from datetime import datetime


class UserService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.mapping_bank_url = {
            'green': 'https://mrcool-greenbank.herokuapp.com/',
            'yellow': 'https://mrcool-yellow.herokuapp.com/',
            'red': 'https://mrcool-redbank.herokuapp.com/',
        }

    def connect_bank(self, token: str, bank: str, login: str, password: str):

        response = requests.get(f'{self.mapping_bank_url[bank]}clients/auth?login={login}&password={password}')
        try:
            data = int(response.json())
        except:
            return None

        user = (
            self.session
                .query(tables.User)
                .filter_by(token=token)
                .first()
        )
        if bank == 'green':
            user.green_bank_id = data
        elif bank == 'yellow':
            user.yellow_bank_id = data
        elif bank == 'red':
            user.red_bank_id = data
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        self.session.commit()
        return True

    def get_id(self, login: str, password: str) -> tables.User:
        user = (
            self.session
                .query(tables.User)
                .filter_by(login=login, password=password)
                .first()
        )
        if user:
            return user.id
        return None

    def get_token(self, login: str, password: str) -> tables.User:
        user = (
            self.session
                .query(tables.User)
                .filter_by(login=login, password=password)
                .first()
        )
        if user:
            return user.token
        return None

    def get_accounts(self, token: str):
        print(token)
        user = (
            self.session
                .query(tables.User)
                .filter_by(token=token)
                .first()
        )
        d = dict()
        if user:
            d['yellow_bank_id'] = user.yellow_bank_id
            d['green_bank_id'] = user.green_bank_id
            d['red_bank_id'] = user.red_bank_id
        else:
            d['yellow_bank_id'] = None
            d['green_bank_id'] = None
            d['red_bank_id'] = None
        return d

    def get_name(self, token: str):
        user = (
            self.session
                .query(tables.User)
                .filter_by(token=token)
                .first()
        )
        if user:
            return user.name
        return None

    def _encoding_user(self, secret: str):
        h = hashlib.new('sha256')
        b = bytes(secret, 'utf-8')
        h.update(b)
        return h.hexdigest()

    def auth_new_user(self, login: str, name: str, password: str):
        new_user = tables.User()
        new_user.login = login
        new_user.name = name
        new_user.password = password
        new_user.token = self._encoding_user(login+name)
        self.session.add(new_user)
        self.session.commit()

        user = (
            self.session
                .query(tables.User)
                .filter_by(login=login, password=password)
                .first()
        )
        return user.token

    def get_account_info(self, url: str, id_client: int):
        account_df = pd.DataFrame(columns=('number', 'type', 'amount'))
        # accounts
        response = requests.get(f'{url}/accounts/client_accounts?id_client={id_client}')
        data = response.json()

        for item in data:
            row = [item['number'], item['type'], item['amount']]
            account_df.loc[len(account_df)] = row

        history_df = pd.DataFrame(columns=('date', 'amount', 'income', 'payment_kind'))

        # history
        response = requests.get(f'{url}/histories/?client_id={id_client}')
        data = response.json()

        for item in data:
            row = [item['date'], item['amount'], item['income'], item['payment_kind']]
            history_df.loc[len(history_df)] = row
        history_df['month'] = history_df['date'].apply(lambda x: pd.to_datetime(x).month)
        return account_df, history_df

    def money_accounts(self, id_green, id_yellow, id_red):

        # green
        green_account_df, _ = pd.DataFrame(columns=('number', 'type', 'amount')), \
                                             pd.DataFrame(columns=('date', 'amount', 'income', 'payment_kind'))
        if id_green:
            green_account_df, _ = self.get_account_info('https://mrcool-greenbank.herokuapp.com', id_green)
        green_account_df['bank'] = 'green'

        # yellow
        yellow_account_df, _ = pd.DataFrame(columns=('number', 'type', 'amount')), \
                                               pd.DataFrame(columns=('date', 'amount', 'income', 'payment_kind'))
        if id_yellow:
            yellow_account_df, _ = self.get_account_info('https://mrcool-yellow.herokuapp.com',
                                                                    id_yellow)
        yellow_account_df['bank'] = 'yellow'

        # red
        red_account_df, _ = pd.DataFrame(columns=('number', 'type', 'amount')), \
                                         pd.DataFrame(columns=('date', 'amount', 'income', 'payment_kind'))
        if id_red:
            red_account_df, _ = self.get_account_info('https://mrcool-redbank.herokuapp.com', id_red)
        red_account_df['bank'] = 'red'

        total_df = pd.concat([green_account_df, yellow_account_df, red_account_df], ignore_index=True)
        return total_df


    def money_history(self, id_green, id_yellow, id_red):

        # green
        _, green_account_df = pd.DataFrame(columns=('number', 'type', 'amount')), \
                                             pd.DataFrame(columns=('date', 'amount', 'income', 'payment_kind'))
        if id_green:
            _, green_account_df = self.get_account_info('https://mrcool-greenbank.herokuapp.com', id_green)
        green_account_df['bank'] = 'green'

        # yellow
        _, yellow_account_df = pd.DataFrame(columns=('number', 'type', 'amount')), \
                                               pd.DataFrame(columns=('date', 'amount', 'income', 'payment_kind'))
        if id_yellow:
            _, yellow_account_df = self.get_account_info('https://mrcool-yellowbank.herokuapp.com', id_yellow)
        yellow_account_df['bank'] = 'yellow'

        # red
        _, red_account_df = pd.DataFrame(columns=('number', 'type', 'amount')), \
                                         pd.DataFrame(columns=('date', 'amount', 'income', 'payment_kind'))
        if id_red:
            _, red_account_df = self.get_account_info('https://mrcool-redbank.herokuapp.com', id_red)
        red_account_df['bank'] = 'red'

        total_df = pd.concat([green_account_df, yellow_account_df, red_account_df], ignore_index=True)
        return total_df


    def money_report(self, id_green, id_yellow, id_red):
        # green
        green_account_df, green_history_df = pd.DataFrame(columns=('number', 'type', 'amount')), \
                                             pd.DataFrame(columns=('date', 'amount', 'income', 'payment_kind'))
        if id_green:
            green_account_df, green_history_df = self.get_account_info('https://mrcool-greenbank.herokuapp.com', id_green)

        # yellow
        yellow_account_df, yellow_history_df = pd.DataFrame(columns=('number', 'type', 'amount')), \
                                               pd.DataFrame(columns=('date', 'amount', 'income', 'payment_kind'))
        if id_yellow:
            yellow_account_df, yellow_history_df = self.get_account_info('https://mrcool-yellowbank.herokuapp.com',
                                                                    id_yellow)

        # red
        red_account_df, red_history_df = pd.DataFrame(columns=('number', 'type', 'amount')), \
                                         pd.DataFrame(columns=('date', 'amount', 'income', 'payment_kind'))
        if id_red:
            red_account_df, red_history_df = self.get_account_info('https://mrcool-redbank.herokuapp.com', id_red)

        total_sum = green_account_df.amount.sum() + yellow_account_df.amount.sum() + red_account_df.amount.sum()
        card_sum = (
                green_account_df.query('type=="card"').amount.sum() +
                yellow_account_df.query('type=="card"').amount.sum() +
                red_account_df.query('type=="card"').amount.sum()
        )
        deposit_sum = (
                green_account_df.query('type=="deposit"').amount.sum() +
                yellow_account_df.query('type=="deposit"').amount.sum() +
                red_account_df.query('type=="deposit"').amount.sum()
        )
        invest_sum = (
                green_account_df.query('type=="invest"').amount.sum() +
                yellow_account_df.query('type=="invest"').amount.sum() +
                red_account_df.query('type=="invest"').amount.sum()
        )
        try:
            green_income_sum = (
                green_history_df.query(f'month=={datetime.now().month} & income==1').amount.sum()
            )
            green_payments_sum = (
                green_history_df.query(f'month=={datetime.now().month} & income==0').amount.sum()
            )
        except:
            green_income_sum, green_payments_sum = 0, 0
        try:
            yellow_income_sum = (
                yellow_history_df.query(f'month=={datetime.now().month} & income==1').amount.sum()
            )
            yellow_payments_sum = (
                yellow_history_df.query(f'month=={datetime.now().month} & income==0').amount.sum()
            )
        except:
            yellow_income_sum, yellow_payments_sum = 0, 0
        try:
            red_income_sum = (
                red_history_df.query(f'month=={datetime.now().month} & income==1').amount.sum()
            )
            red_payments_sum = (
                red_history_df.query(f'month=={datetime.now().month} & income==0').amount.sum()
            )
        except:
            red_income_sum, red_payments_sum = 0, 0
        total_income_sum = (
                green_income_sum + yellow_income_sum + red_income_sum
        )
        total_payments_sum = (
                green_payments_sum + yellow_payments_sum + red_payments_sum
        )

        total_names = ['Доходы', 'Расходы', 'Депозиты', 'Инвестиции']
        total_values = [green_income_sum, card_sum, deposit_sum, invest_sum]

        common_names = ['Доходы', 'Расходы']
        green_values = [green_income_sum, green_payments_sum]
        yellow_values = [yellow_income_sum, yellow_payments_sum]
        red_values = [red_income_sum, red_payments_sum]
        total_detailed_values = [total_income_sum, total_payments_sum]

        # detailed table
        detailed_items = []
        for i in range(len(common_names)):
            an_item = dict(c1=common_names[i], c2=total_detailed_values[i])
            detailed_items.append(an_item)
        # green_detailed table
        greens_detailed_items = []
        for i in range(len(common_names)):
            an_item = dict(c1=common_names[i], c2=green_values[i])
            greens_detailed_items.append(an_item)

        # yellow_detailed table
        yellow_detailed_items = []
        for i in range(len(common_names)):
            an_item = dict(c1=common_names[i], c2=yellow_values[i])
            yellow_detailed_items.append(an_item)

        # red_detailed table
        red_detailed_items = []
        for i in range(len(common_names)):
            an_item = dict(c1=common_names[i], c2=red_values[i])
            red_detailed_items.append(an_item)

        # total table
        total_items = []
        for i in range(len(total_names)):
            an_item = dict(c1=total_names[i], c2=total_values[i])
            total_items.append(an_item)

        # green table
        green_items = []
        for i in range(green_account_df.shape[0]):
            an_item = dict(c1=green_account_df.loc[i, 'number'], c2=green_account_df.loc[i, 'type'],
                           c3=green_account_df.loc[i, 'amount'])
            green_items.append(an_item)

        # yellow table
        yellow_items = []
        for i in range(yellow_account_df.shape[0]):
            an_item = dict(c1=yellow_account_df.loc[i, 'number'], c2=yellow_account_df.loc[i, 'type'],
                           c3=yellow_account_df.loc[i, 'amount'])
            yellow_items.append(an_item)

        # red table
        red_items = []
        for i in range(red_account_df.shape[0]):
            an_item = dict(c1=red_account_df.loc[i, 'number'], c2=red_account_df.loc[i, 'type'],
                           c3=red_account_df.loc[i, 'amount'])
            red_items.append(an_item)

        report_dict = dict()
        report_dict['total_items'] = total_items
        report_dict['green_items'] = green_items
        report_dict['yellow_items'] = yellow_items
        report_dict['red_items'] = red_items
        report_dict['detailed_items'] = detailed_items
        report_dict['greens_detailed_items'] = greens_detailed_items
        report_dict['yellow_detailed_items'] = yellow_detailed_items
        report_dict['red_detailed_items'] = red_detailed_items
        return report_dict






