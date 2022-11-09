from typing import List
from fastapi import Depends

import pickle
import os

from ..database import Session, get_session
from .. import tables

class ClientService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get_total_incomes(self):


    def get_common(self, client_id: int) -> tables.Client:
        query = self.session.query(tables.Client)
        client = (
            self.session
                .query(tables.Client)
                .filter_by(client_id=client_id)
                .first()
        )



        return budgets

    def predict(self) -> List[float]:
        query = self.session.query(tables.Budget)

        X_predict = [[q.f1, q.f2] for q in query]
        predictions = list(self.model.predict(X_predict))
        return predictions

    def total_table(self) -> dict:
        query = self.session.query(tables.Budget)

        fact_values = [[q.f1, q.f2, q.amount] for q in query]
        X_predict = [[q.f1, q.f2] for q in query]
        predictions = [[i] for i in self.model.predict(X_predict)]

        fact_df = pd.DataFrame(fact_values, columns=['fact_1','fact_2','amount'])
        fact_df['is_predict'] = 0

        preds_df = pd.DataFrame([item + pred for item, pred in zip(X_predict, predictions)], columns=['fact_1','fact_2','amount'])
        preds_df['is_predict'] = 1

        total_df = pd.concat([fact_df, preds_df], axis=0, ignore_index=True)

        total_dict = dict()
        total_dict['df'] = total_df
        return total_dict
