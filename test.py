class Criterion:
    """An abstract class representing a criterion used to evaluate the quality
    of a group based on the group members' answers for a given question.
    """

    def score_answers(self, question: Question, answers: list[Answer]) -> float:
        """Return score between 0.0 and 1.0 indicating how well the group
        of <answers> to the question <question> satisfy this Criterion.

        Raise InvalidAnswerError if any answer in <answers> is not a valid
        answer to <question>.

        Each implementation of this abstract class will measure satisfaction of
        a criterion differently.
        """
        raise NotImplementedError
