from UserResponseMatchingAndRewarding.models import UserResponseScore
from TestingSystem.models import TestQuestionRandomizeModel
from datetime import timedelta
import pandas as pd
import numpy as np
import pytz


class AnalyseUtils:
    def __init__(self, users) -> None:
        self.users = users

    def _result(self):
        user_info = dict()
        for user in self.users:
            try:
                UTP = None
                URS = UserResponseScore.objects.get(user=user)
                user_info[user] = dict(
                    percentage=URS.persentage,
                    score=f"{URS.score}/{URS.ranks}",
                    spent_time=f"{UTP.spent_time.hour}:{UTP.spent_time.minute}:{UTP.spent_time.second}",
                    completed_date=UTP.ended_time.astimezone(
                        pytz.timezone("Asia/Tashkent")
                    ).strftime("%b %d,%Y at %I:%M%p"),
                )
            except:
                pass
        return user_info

    def _durationsAvarege(self, durations) -> str:
        total_duration = sum(durations, timedelta())
        mean_duration = total_duration / len(durations)
        mean_seconds = mean_duration.total_seconds()
        mean_hours, remainder = divmod(mean_seconds, 3600)
        mean_minutes, mean_seconds = divmod(remainder, 60)
        mean_duration_str = (
            f"{int(mean_hours):02d}:{int(mean_minutes):02d}:{int(mean_seconds):02d}"
        )
        return mean_duration_str

    def _statistic(self) -> dict:
        results = self._result().items()
        avarege_percentage = np.round(
            np.mean([result["percentage"] for user, result in results]), 1
        )
        avarege_score = np.round(
            np.mean([int(result["score"].split("/")[0]) for user, result in results]), 1
        )
        durations = [
            timedelta(
                hours=int(result["spent_time"].split(":")[0]),
                minutes=int(result["spent_time"].split(":")[1]),
                seconds=int(result["spent_time"].split(":")[2]),
            )
            for user, result in results
        ]
        mean_duration_str = self._durationsAvarege(durations)
        statistics = dict(
            avarege_percentage=avarege_percentage,
            avarege_score=avarege_score,
            mean_duration=mean_duration_str,
            users=len(self._result()),
        )
        return statistics


class Analyse(AnalyseUtils):
    def __init__(self, model) -> None:
        super(Analyse, self).__init__(model.user_assign.all())

    def Result(self) -> dict:
        return self._result()

    def Statistic(self) -> dict:
        if self.users:
            return self._statistic()
        return False


class CopyUtils:
    def __init__(self, model) -> None:
        self.model = model


class CopyLink(CopyUtils):
    def __init__(self, model, link) -> None:
        super(CopyLink, self).__init__(model)
        self.link = link

    def GivenLink(self) -> str:
        return self.link.format(self.model.slug_field)


class LinkUtils:
    def __init__(self, post, key):
        self.post_request = post
        self.post_key = key

    def check_id(self, current_id):
        """
        Check if the current ID matches the ID in the post.
        """
        confirmed_id = self.post_request.get(self.post_key, None)
        if confirmed_id is not None:
            try:
                return int(confirmed_id) == current_id
            except ValueError:
                # If the confirmed ID is not a number, return False.
                return False
        return False


class DeleteConfirmedLink(LinkUtils):
    def __init__(self, post, key, model) -> None:
        super(DeleteConfirmedLink, self).__init__(post, key)
        self.model = model

    def DeleteLink(self) -> bool:
        model = self.model
        if self.check_id(self.model.id):
            model.delete()
            return True
        return False


class SortUtils:
    def __init__(self, data) -> None:
        self.data = data
        self.dataframe = pd.DataFrame.from_dict(self.data, orient="index")

    def _embedingColumn(self, order_by):
        df = self.dataframe
        if "Test_name" == order_by:
            df[order_by] = [i.title for i in df.index.values]
        elif "Link_name" == order_by:
            df[order_by] = [i.assign_name for i in df.index.values]
        elif "name" == order_by:
            df[order_by] = [i.name for i in df.index.values]
        return df

    def _sortItPandas(self, order_by, order) -> dict:
        df = self._embedingColumn(order_by)
        sorted_order = df.sort_values(by=order_by, ascending=order).to_dict(
            orient="index"
        )
        return sorted_order


class SortBy(SortUtils):
    def __init__(self, data) -> None:
        super(SortBy, self).__init__(data)

    def sortDescAsc(self, order_by="percentage", order=False) -> dict:
        return self._sortItPandas(order_by=order_by, order=order)
