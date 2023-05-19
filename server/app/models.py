from typing import Optional

from pydantic import BaseModel

import pandas as pd


class UserData(BaseModel):
    id: str
    age: int
    sex: int
    height: int
    weight: int
    fat: int
    sleep: Optional[int]
    cls: int

    def to_dataframe(self):
        return pd.DataFrame(
            {
                'Age': [self.age],
                'Sex': [self.sex],
                'Height': [self.height],
                'Weight': [self.weight],
                'ProcFat': [self.fat],
                'Sleep': [self.sleep],
                'Class': [self.cls]
            }
        )


class TrainData(BaseModel):
    id: str

    pull_ups: int
    sum_pullups: int

    push_ups: int
    sum_pushups: int

    squats: int
    sum_squats: int


class ScoreResponse(BaseModel):
    pushups: int
    pullups: int
    squats: int
