# TODO: Add the test cases that you'll be submitting to this file!
#       Make sure your test cases are all named starting with
#       test_ and that they have unique names.

# You may need to import pytest in order to run your tests.
# You are free to import hypothesis and use hypothesis for testing.
# This file will not be graded for style with PythonTA
import pytest
from course import Student, Course
from survey import Question, MultipleChoiceQuestion, NumericQuestion, \
    YesNoQuestion, CheckboxQuestion, Answer, Survey
from criterion import Criterion, HomogeneousCriterion, HeterogeneousCriterion, \
    LonelyMemberCriterion, InvalidAnswerError
from grouper import Group, Grouping, Grouper, AlphaGrouper, GreedyGrouper, \
    SimulatedAnnealingGrouper
from hypothesis import given, strategies as st

###############################################################################
# Task 2 Test cases
###############################################################################
class TestStudent:

    def test_name(self) -> None:
        student = Student(1, 'Anthony')
        assert student.name == 'Anthony'

    def test_id(self) -> None:
        student = Student(1, 'Anthony')
        assert student.id == 1

    @given(id_=st.integers(min_value=1), name=st.text())
    def test_new_student_answers(self, id_: int, name: str) -> None:
        student = Student(id_, name)
        assert student._answers == {}

    def test_has_answer_with_answer(self) -> None:
        student = Student(1, 'Anthony')
        question = MultipleChoiceQuestion(1, 'Make a choice:', ['1', '2', '3'])
        answer = Answer('2')
        student.set_answer(question, answer)
        assert student.has_answer(question) is True

    def test_has_answer_without_answer(self) -> None:
        student = Student(1, 'Anthony')
        question1 = MultipleChoiceQuestion(1, 'Make a choice:', ['1', '2', '3'])
        question2 = MultipleChoiceQuestion(2, 'Make a choice:', ['1', '2', '3'])
        answer = Answer('2')
        student.set_answer(question1, answer)
        assert student.has_answer(question2) is False

    def test_set_answer(self) -> None:
        student = Student(1, 'Anthony')
        question = MultipleChoiceQuestion(1, 'Make a choice:', ['1', '2', '3'])
        answer = Answer('2')
        student.set_answer(question, answer)
        assert student._answers[1] == answer

    def test_set_answer_override(self) -> None:
        student = Student(1, 'Anthony')
        question = MultipleChoiceQuestion(1, 'Make a choice:', ['1', '2', '3'])
        answer1 = Answer('2')
        answer2 = Answer('3')
        student.set_answer(question, answer1)
        student.set_answer(question, answer2)
        assert student._answers[1] == answer2

    def test_set_answer_mutiple_questions_and_answers(self) -> None:
        student = Student(1, 'Anthony')
        question1 = MultipleChoiceQuestion(
            1, 'Make a choice:', ['1', '2', '3'])
        question2 = NumericQuestion(2, 'Choose an integer:', 0, 10)
        question3 = YesNoQuestion(3, 'True or False:')
        question4 = CheckboxQuestion(4, 'Make a choice:', ['1', '2', '3', '4'])
        answer1 = Answer('2')
        answer2 = Answer(1)
        answer3 = Answer(True)
        answer4 = Answer(['2', '3'])
        student.set_answer(question1, answer1)
        student.set_answer(question2, answer2)
        student.set_answer(question3, answer3)
        student.set_answer(question4, answer4)
        assert student._answers[1] == answer1
        assert student._answers[2] == answer2
        assert student._answers[3] == answer3
        assert student._answers[4] == answer4

    def test_get_answer(self) -> None:
        student = Student(1, 'Anthony')
        question = MultipleChoiceQuestion(1, 'Make a choice:', ['1', '2', '3'])
        answer = Answer('2')
        student.set_answer(question, answer)
        assert student.get_answer(question) == answer

    def test_get_answer_no_answer(self) -> None:
        student = Student(1, 'Anthony')
        question = MultipleChoiceQuestion(1, 'Make a choice:', ['1', '2', '3'])
        assert student.get_answer(question) is None

###############################################################################
# Task 3 Test cases
###############################################################################
class TestCourse:

    def test_name(self) -> None:
        course = Course('CSC148')
        assert course.name == 'CSC148'

    @given(name=st.text())
    def test_new_course_students_list(self, name: str) -> None:
        course = Course('CSC148')
        assert course.students == []

    def test_enroll_students_with_empty_students(self) -> None:
        std1 = Student(1, 'Kevin')
        std2 = Student(2, 'James')
        std3 = Student(3, 'Baston')
        course = Course('CSC148')
        course.enroll_students(std_list := [std1, std2, std3])
        assert course.students == std_list

    def test_enroll_students_with_empty_string_name(self) -> None:
        std1 = Student(1, 'Kevin')
        std2 = Student(2, 'James')
        std3 = Student(3, '')
        course = Course('CSC148')
        course.enroll_students([std1, std2, std3])
        assert course.students == []

    def test_enroll_students_with_same_id(self) -> None:
        std1 = Student(1, 'Kevin')
        std2 = Student(2, 'James')
        std3 = Student(3, 'Baston')
        course = Course('CSC148')
        course.enroll_students(std_list := [std1, std2, std3])
        course.enroll_students([std1])
        assert course.students == std_list

    def test_all_answered_1(self) -> None:
        std1 = Student(1, 'Kevin')
        course = Course('CSC148') 
        course.enroll_students([std1])
        question1 = NumericQuestion(1, 'Make a choice:', -10, 10)
        question2 = YesNoQuestion(2, 'Make a choice:')
        survey = Survey([question1, question2])
        assert course.all_answered(survey) is False

    def test_all_answered_2(self) -> None:
        std1 = Student(1, 'Kevin')
        course = Course('CSC148') 
        course.enroll_students([std1])
        question1 = NumericQuestion(1, 'Make a choice:', -10, 10)
        answer1 = Answer(0)
        question2 = YesNoQuestion(2, 'Make a choice:')
        answer2 = Answer(False) 
        std1.set_answer(question1, answer1)
        std1.set_answer(question2, answer2)
        survey = Survey([question1, question2])
        assert course.all_answered(survey) is True

    def test_get_students(self) -> None:
        std1 = Student(1, 'Kevin')
        std2 = Student(2, 'James')
        std3 = Student(3, 'Baston')
        course = Course('CSC148')
        course.enroll_students([std2, std1, std3])
        assert course.get_students() == (std1, std2, std3)


###############################################################################
# Task 4 Test cases
###############################################################################
class TestMultipleChoiceQuestion:

    def test_id(self) -> None:
        question = MultipleChoiceQuestion(1, 'Make a choice:', ['1', '2', '3'])
        assert question.id == 1

    def test_text(self) -> None:
        question = MultipleChoiceQuestion(1, 'Make a choice:', ['1', '2', '3'])
        assert question.text == 'Make a choice:'

    def test_options(self) -> None:
        question = MultipleChoiceQuestion(1, 'Make a choice:', ['1', '2', '3'])
        assert question._options == ['1', '2', '3']

    def test_validate_answer_1(self) -> None:
        question = MultipleChoiceQuestion(1, 'Make a choice:', ['1', '2', '3'])
        answer = Answer('1')
        assert question.validate_answer(answer) is True

    def test_validate_answer_2(self) -> None:
        question = MultipleChoiceQuestion(1, 'Make a choice:', ['1', '2', '3'])
        answer = Answer('ok')
        assert question.validate_answer(answer) is False

    def test_validate_answer_worksheet(self) -> None:
        question = MultipleChoiceQuestion(1, 'q2:', ['Victoria', 'New', 'Woodsworth', 'Trinity'])
        answer = Answer('Woodsworth')
        assert question.validate_answer(answer) is True

    def test_get_similarity(self) -> None:
        question = MultipleChoiceQuestion(1, 'Make a choice:', ['1', '2', '3'])
        answer1 = Answer('1')
        answer2 = Answer('1')
        assert question.get_similarity(answer1, answer2) == 1.0


class TestNumericQuestion:

    def test_id(self) -> None:
        question = NumericQuestion(1, 'Choose an integer:', 0, 10)
        assert question.id == 1

    def test_text(self) -> None:
        question = NumericQuestion(1, 'Choose an integer:', 0, 10)
        assert question.text == 'Choose an integer:'

    def test_max_and_min(self) -> None:
        question = NumericQuestion(1, 'Choose an integer:', 0, 10)
        assert question._max_ == 10
        assert question._min_ == 0

    def test_validate_answer(self) -> None:
        question = NumericQuestion(1, 'Choose an integer:', 0, 10)
        answer = Answer(10)
        assert question.validate_answer(answer) is True

    def test_get_similarity(self) -> None:
        question = NumericQuestion(1, 'Choose an integer:', 0, 10)
        answer1 = Answer(0)
        answer2 = Answer(1)
        assert question.get_similarity(answer1, answer2) == 0.9


class TestYesNoQuestion:

    def test_id(self) -> None:
        question = YesNoQuestion(1, 'True or False:')
        assert question.id == 1

    def test_text(self) -> None:
        question = YesNoQuestion(1, 'True or False:')
        assert question.text == 'True or False:'

    def test_validate_answer(self) -> None:
        question = YesNoQuestion(1, 'True or False:')
        answer = Answer(True)
        assert question.validate_answer(answer) is True

    def test_validate_answer_not_yes_or_no(self) -> None:
        question = YesNoQuestion(1, 'True or False:')
        answer = Answer('Yes')
        assert question.validate_answer(answer) is False

    def test_get_similarity(self) -> None:
        question = YesNoQuestion(1, 'True or False:')
        answer1 = Answer(True)
        answer2 = Answer(False)
        assert question.get_similarity(answer1, answer2) == 0.0


class TestCheckboxQuestion:

    def test_id(self) -> None:
        question = CheckboxQuestion(1, 'Make a choice:', ['1', '2', '3', '4'])
        assert question.id == 1

    def test_text(self) -> None:
        question = CheckboxQuestion(1, 'Make a choice:', ['1', '2', '3', '4'])
        assert question.text == 'Make a choice:'

    def test_options(self) -> None:
        question = CheckboxQuestion(1, 'Make a choice:', ['1', '2', '3', '4'])
        assert question._options == ['1', '2', '3', '4']

    def test_validate_answer(self) -> None:
        question = CheckboxQuestion(1, 'Make a choice:', ['1', '2', '3', '4'])
        answer = Answer(['1', '2'])
        assert question.validate_answer(answer) is True

    def test_validate_answer_random_order(self) -> None:
        question = CheckboxQuestion(1, 'Make a choice:', ['1', '2', '3', '4'])
        answer = Answer(['3', '1', '4', '2'])
        assert question.validate_answer(answer) is True

    def test_validate_answer_with_empty_list(self) -> None:
        question = CheckboxQuestion(1, 'Make a choice:', ['1', '2', '3', '4'])
        answer = Answer([])
        assert question.validate_answer(answer) is False

    def test_validate_answer_with_duplicate_entries(self) -> None:
        question = CheckboxQuestion(1, 'Make a choice:', ['1', '2', '3', '4'])
        answer = Answer(['2', '1', '1'])
        assert question.validate_answer(answer) is False

    def test_validate_answer_with_not_included_item(self) -> None:
        question = CheckboxQuestion(1, 'Make a choice:', ['1', '2', '3', '4'])
        answer = Answer(['1', '2', '3', '5'])
        assert question.validate_answer(answer) is False

    def test_get_similarity(self) -> None:
        question = CheckboxQuestion(1, 'Make a choice:', ['1', '2', '3', '4'])
        answer1 = Answer(['1', '3', '5', '7', '9'])
        answer2 = Answer(['2', '1', '3', '5'])
        assert question.get_similarity(answer1, answer2) == 0.5

###############################################################################
# Task 5 Test cases
###############################################################################
class TestAnswer:

    def test_is_valid_with_mutltiple_choice_question(self) -> None:
        question = MultipleChoiceQuestion(1, 'Make a choice:', ['a', 'b', 'c'])
        answer = Answer('c')
        assert answer.is_valid(question) is True

    def test_is_valid_with_numeric_question(self) -> None:
        question = NumericQuestion(1, 'Make a choice:', -10, 10)
        answer = Answer(1)
        assert answer.is_valid(question) is True

    def test_is_valid_with_yes_no_question(self) -> None:
        question = YesNoQuestion(1, 'Make a choice:')
        answer = Answer(False)
        assert answer.is_valid(question) is True

    def test_is_valid_with_checkbox_question(self) -> None:
        question = CheckboxQuestion(1, 'Make a choice:', ['a', 'b', 'c'])
        answer = Answer(['a', 'c'])
        assert answer.is_valid(question) is True


###############################################################################
# Task 6 Test cases
###############################################################################
class TestHomogeneousCriterion:

    def test_score_answers_invalid_answer(self) -> None:
        criterion = HomogeneousCriterion()
        question = CheckboxQuestion(1, 'Make a choice:', ['1', '2', '3', '4'])
        answer1, answer2 = Answer(['1', '2', '3', '4']), Answer(['5'])
        with pytest.raises(InvalidAnswerError) as error:
            criterion.score_answers(question, [answer1, answer2])
        assert error.type == InvalidAnswerError

    def test_score_answers_single_answer(self) -> None:
        criterion = HomogeneousCriterion()
        question = CheckboxQuestion(1, 'Make a choice:', ['1', '2', '3', '4'])
        answer = Answer(['1', '2', '3', '4'])
        assert criterion.score_answers(question, [answer]) == 1.0

    def test_score_answers_mutiple_answers(self) -> None:
        criterion = HomogeneousCriterion()
        question = CheckboxQuestion(1, 'input:', ['1', '2', '3', '4', '5'])
        answer1 = Answer(['1', '2'])
        answer2 = Answer(['1', '3'])
        answer3 = Answer(['1', '4'])
        assert criterion.score_answers(
                        question, [answer1, answer2, answer3]) == (1 / 3)

    def test_score_answers_worksheet(self) -> None:
        criterion = HomogeneousCriterion()
        question1 = NumericQuestion(1, 'q1:', 1, 6)
        answer1 = Answer(3)
        answer2 = Answer(2)
        answer3 = Answer(3)
        answer4 = Answer(3)
        assert pytest.approx(criterion.score_answers(
            question1, [answer1, answer2, answer3, answer4])) == (9 / 10)


class TestHeterogeneousCriterion:

    def test_score_answers_invalid_answer(self) -> None:
        criterion = HeterogeneousCriterion()
        question = CheckboxQuestion(1, 'Make a choice:', ['1', '2', '3', '4'])
        answer1, answer2 = Answer(['1', '2', '3', '4']), Answer(['5'])
        with pytest.raises(InvalidAnswerError) as error:
            criterion.score_answers(question, [answer1, answer2])
        assert error.type == InvalidAnswerError

    def test_score_answers_single_answer(self) -> None:
        criterion = HeterogeneousCriterion()
        question = CheckboxQuestion(1, 'Make a choice:', ['1', '2', '3', '4'])
        answer = Answer(['1', '2', '3', '4'])
        assert criterion.score_answers(question, [answer]) == 0.0

    def test_score_answers_mutiple_answers(self) -> None:
        criterion = HeterogeneousCriterion()
        question = CheckboxQuestion(1, 'input:', ['1', '2', '3', '4', '5'])
        answer1 = Answer(['1', '2'])
        answer2 = Answer(['1', '3'])
        answer3 = Answer(['1', '4'])
        assert round(criterion.score_answers(
                        question, [answer1, answer2, answer3]), 2) == 0.67 


class TestLonelyMemberCriterion:

    def test_score_answers_invalid_answer(self) -> None:
        criterion = LonelyMemberCriterion()
        question = CheckboxQuestion(1, 'Make a choice:', ['1', '2', '3', '4'])
        answer1, answer2 = Answer(['1', '2', '3', '4']), Answer(['5'])
        with pytest.raises(InvalidAnswerError) as error:
            criterion.score_answers(question, [answer1, answer2])
        assert error.type == InvalidAnswerError

    def test_score_answers_single_answer(self) -> None:
        criterion = LonelyMemberCriterion()
        question = CheckboxQuestion(1, 'Make a choice:', ['1', '2', '3', '4'])
        answer = Answer(['1', '2', '3', '4'])
        assert criterion.score_answers(question, [answer]) == 0.0

    def test_score_answers_unique_answer(self) -> None:
        criterion = LonelyMemberCriterion()
        question = CheckboxQuestion(1, 'input:', ['1', '2', '3', '4', '5'])
        answer1 = Answer(['1', '2'])
        answer2 = Answer(['1', '3'])
        answer3 = Answer(['1', '2'])
        assert criterion.score_answers(
                        question, [answer1, answer2, answer3]) == 0.0

    def test_score_answers_common_answers(self) -> None:
        criterion = LonelyMemberCriterion()
        question = CheckboxQuestion(1, 'input:', ['1', '2', '3', '4', '5'])
        answer1 = Answer(['1', '2'])
        answer2 = Answer(['1', '2'])
        answer3 = Answer(['1', '3'])
        answer4 = Answer(['1', '3'])
        assert criterion.score_answers(
                        question, [answer1, answer2, answer3, answer4]) == 1.0

    def test_score_answers_worksheet(self) -> None:
        criterion = LonelyMemberCriterion()
        question2 = MultipleChoiceQuestion(2, 'q2:', ['Victoria', 'New', 'Woodsworth', 'Trinity'])
        answer1 = Answer('Woodsworth')
        answer2 = Answer('Woodsworth')
        answer3 = Answer('Woodsworth')
        assert criterion.score_answers(
                        question2, [answer1, answer2, answer3]) == 1.0

###############################################################################
# Task 7 Test cases
###############################################################################
class TestGroup:

    def test___len__1(self) -> None:
        student1 = Student(1, 'Anthony')
        student2 = student1
        student3 = Student(2, 'Anthony')
        group = Group([student1, student2, student3])
        assert len(group._members) == 2

    def test___len__2(self) -> None:
        student1 = Student(1, 'Anthony')
        student2 = Student(2, 'Anthony')
        student3 = Student(3, 'Anthony')
        group = Group([student1, student2, student3])
        assert len(group._members) == 3

    def test___contains__1(self) -> None:
        student1 = Student(1, 'Anthony')
        student2 = Student(2, 'James')
        student3 = Student(3, 'Anthony')
        group = Group([student1, student2, student3])
        assert group.__contains__(student3) is True
    
    def test___contains__2(self) -> None:
        student1 = Student(1, 'Anthony')
        student2 = Student(2, 'James')
        student3 = Student(3, 'Anthony')
        group = Group([student1, student2])
        assert group.__contains__(student3) is False

    def test_get_members(self) -> None:
        student1 = Student(1, 'Anthony')
        student2 = Student(2, 'James')
        student3 = Student(3, 'Kevin')
        group = Group(group_list := [student1, student2, student3])
        assert group.get_members() == [student1, student2, student3]

    def test_get_members_no_mutation(self) -> None:
        student1 = Student(1, 'Anthony')
        student2 = Student(2, 'James')
        student3 = Student(3, 'Kevin')
        group = Group(group_list := [student1, student2, student3])
        group.get_members().append([1, 2, 3])
        assert group.get_members() == group_list

###############################################################################
# Task 8 Test cases
###############################################################################
class TestGrouping:

    def test_add_group(self) -> None: 
        student1 = Student(1, 'Anthony')
        student2 = Student(2, 'James')
        student3 = Student(3, 'Kevin')
        groups = Grouping()
        group1 = Group([student1, student3])
        assert groups.add_group(group1) is True
        group2 = Group([student2])
        assert groups.add_group(group2) is True

    def test_add_group_with_a_group_contains_no_member(self) -> None:
        group = Group([])
        groups = Grouping()
        assert groups.add_group(group) is False

    def test_add_group_with_same_id(self) -> None: 
        student1 = Student(1, 'Anthony')
        student2 = Student(2, 'James')
        student3 = Student(3, 'Kevin')
        groups = Grouping()
        group1 = Group([student1, student2, student3])
        assert groups.add_group(group1) is True
        group2 = Group([student1])
        assert groups.add_group(group2) is False
        group3 = Group([student2, student3])
        assert groups.add_group(group3) is False

    def test___len__(self) -> None:
        student1 = Student(1, 'Anthony')
        student2 = Student(2, 'James')
        student3 = Student(3, 'Kevin')
        grouping = Grouping()
        group1 = Group([student1, student3])
        grouping.add_group(group1)
        group2 = Group([student2])
        grouping.add_group(group2)
        assert len(grouping) == 2

    def test_get_groups(self) -> None:
        student1 = Student(1, 'Anthony')
        student2 = Student(2, 'James')
        student3 = Student(3, 'Kevin')
        group1 = Group([student1])
        group2 = Group([student2])
        group3 = Group([student3])
        grouping = Grouping()
        grouping.add_group(group1)
        grouping.add_group(group2)
        grouping.add_group(group3)
        assert grouping.get_groups() == [group1, group2, group3]

    def test_get_groups_no_mutation_1(self) -> None:
        student1 = Student(1, 'Anthony')
        student2 = Student(2, 'James')
        student3 = Student(3, 'Kevin')
        group1 = Group([student1])
        group2 = Group([student2])
        group3 = Group([student3])
        grouping = Grouping()
        grouping.add_group(group1)
        grouping.add_group(group2)
        grouping.add_group(group3)
        grouping.get_groups().append('Test Mutation')
        assert grouping.get_groups() == [group1, group2, group3]

    def test_get_groups_no_mutation_2(self) -> None:
        student1 = Student(1, 'Anthony')
        student2 = Student(2, 'James')
        student3 = Student(3, 'Kevin')
        group1 = Group([student1])
        grouping = Grouping()
        grouping.add_group(group1)
        grouping.get_groups()[0].get_members().append('Test Mutation')
        assert grouping.get_groups() == [group1]

###############################################################################
# Task 9 Test cases
###############################################################################
class TestSurvey:

    def test_same_dict_id(self) -> None:
        question1 = NumericQuestion(1, 'Make a choice:', -10, 10)
        survey = Survey([question1])
        assert survey._weights.keys() == survey._criteria.keys(
                                                   ) == survey._questions.keys()

    def test_get_questions(self) -> None:
        question1 = NumericQuestion(1, 'Make a choice:', -10, 10)
        question2 = YesNoQuestion(2, 'Make a choice:')
        survey = Survey(lst := [question1, question2])
        assert survey.get_questions() == lst

    def test__get_criterion(self) -> None:
        question1 = NumericQuestion(1, 'Make a choice:', -10, 10)
        survey = Survey([question1])
        assert isinstance(survey._get_criterion(question1), HomogeneousCriterion)

    def test__get_weight(self) -> None:
        question1 = NumericQuestion(1, 'Make a choice:', -10, 10)
        survey = Survey([question1])
        assert survey._get_weight(question1) == 1

    def test_set_weight(self) -> None:
        question1 = NumericQuestion(1, 'Make a choice:', -10, 10)
        survey = Survey([question1])
        survey.set_weight(2, question1)
        assert survey._get_weight(question1) == 2

    def test_set_weight_id_not_included(self) -> None:
        question1 = NumericQuestion(1, 'Make a choice:', -10, 10)
        survey = Survey([question1])
        question2 = NumericQuestion(2, 'Make a choice:', 0, 10)
        survey.set_weight(2, question2)
        assert survey._weights.get(2) == None

    def test_set_criterion(self) -> None:
        question1 = NumericQuestion(1, 'Make a choice:', -10, 10)
        survey = Survey([question1])
        survey.set_criterion((criterion := HeterogeneousCriterion()), question1)
        assert survey._get_criterion(question1) == criterion

    def test_set_criterion_id_not_included(self) -> None:
        question1 = NumericQuestion(1, 'Make a choice:', -10, 10)
        survey = Survey([question1])
        question2 = NumericQuestion(2, 'Make a choice:', 0, 10)
        survey.set_criterion(2, question2)
        assert survey._criteria.get(2) == None

    def test_score_students_invalid_answer(self) -> None:
        std1 = Student(1, 'Kevin')
        question1 = NumericQuestion(1, 'Make a choice:', 1, 10)
        answer = Answer(0)
        std1.set_answer(question1, answer)
        survey = Survey([question1])
        assert survey.score_students([std1]) == 0.0

    def test_score_students_empty_questions(self) -> None:
        std1 = Student(1, 'Kevin')
        survey = Survey([])
        assert survey.score_students([std1]) == 0.0

    def test_score_students_worksheet_1(self) -> None:
        question2 = MultipleChoiceQuestion(2, 'q2:', ['Victoria', 'New', 'Woodsworth', 'Trinity'])
        survey = Survey([question2])
        survey.set_weight(20, question2)
        survey.set_criterion(LonelyMemberCriterion(), question2)
        std9 = Student(9, 'Grace')
        std9.set_answer(question2, Answer('Woodsworth'))
        std10 = Student(10, 'Claire')
        std10.set_answer(question2, Answer('Woodsworth'))
        std11 = Student(11, 'Kai')
        std11.set_answer(question2, Answer('Woodsworth')) 
        assert survey.score_students([std9, std10, std11]) == 20

    def test_score_students_worksheet_2(self) -> None:
        question1 = NumericQuestion(1, 'q1:', 1, 6)
        question2 = MultipleChoiceQuestion(2, 'q2:', ['Victoria', 'New', 'Woodsworth', 'Trinity'])
        survey = Survey([question1, question2])
        survey.set_weight(80, question1)
        survey.set_weight(20, question2)
        survey.set_criterion(LonelyMemberCriterion(), question2)
        std1 = Student(1, 'Pyria')
        std1.set_answer(question1, Answer(3))
        std1.set_answer(question2, Answer('Victoria'))
        std2 = Student(2, 'Alain')
        std2.set_answer(question1, Answer(2))
        std2.set_answer(question2, Answer('New'))
        std3 = Student(3, 'Zoe')
        std3.set_answer(question1, Answer(3))
        std3.set_answer(question2, Answer('Woodsworth'))
        std4 = Student(4, 'Francesco')
        std4.set_answer(question1, Answer(3))
        std4.set_answer(question2, Answer('Victoria'))
        assert survey.score_students([std1, std2, std3, std4]) == 36

    def test_score_grouping_empty_grouping(self) -> None:
        survey = Survey([])
        grouping = Grouping()
        assert survey.score_grouping(grouping) == 0.0

    def test_score_grouping_worksheet(self) -> None:
        question1 = NumericQuestion(1, 'q1:', 1, 6)
        question2 = MultipleChoiceQuestion(2, 'q2:', ['Victoria', 'New', 'Woodsworth', 'Trinity'])
        survey = Survey([question1, question2])
        survey.set_weight(80, question1)
        survey.set_weight(20, question2)
        survey.set_criterion(LonelyMemberCriterion(), question2)
        std1 = Student(1, 'Pyria')
        std1.set_answer(question1, Answer(3))
        std1.set_answer(question2, Answer('Victoria'))
        std2 = Student(2, 'Alain')
        std2.set_answer(question1, Answer(2))
        std2.set_answer(question2, Answer('New'))
        std3 = Student(3, 'Zoe')
        std3.set_answer(question1, Answer(3))
        std3.set_answer(question2, Answer('Woodsworth'))
        std4 = Student(4, 'Francesco')
        std4.set_answer(question1, Answer(3))
        std4.set_answer(question2, Answer('Victoria'))
        group1 = Group([std1, std2, std3, std4])
        std5 = Student(5, 'Mohammed')
        std5.set_answer(question1, Answer(4))
        std5.set_answer(question2, Answer('Woodsworth'))
        std6 = Student(6, 'Xiaoyuan')
        std6.set_answer(question1, Answer(5))
        std6.set_answer(question2, Answer('New'))
        std7 = Student(7, 'Rohit')
        std7.set_answer(question1, Answer(2))
        std7.set_answer(question2, Answer('New'))
        std8 = Student(8, 'Yimin')
        std8.set_answer(question1, Answer(3))
        std8.set_answer(question2, Answer('Trinity'))
        group2 = Group([std5, std6, std7, std8])
        std9 = Student(9, 'Grace')
        std9.set_answer(question1, Answer(5))
        std9.set_answer(question2, Answer('Woodsworth'))
        std10 = Student(10, 'Claire')
        std10.set_answer(question1, Answer(1))
        std10.set_answer(question2, Answer('Woodsworth'))
        std11 = Student(11, 'Kai')
        std11.set_answer(question1, Answer(1))
        std11.set_answer(question2, Answer('Woodsworth'))
        group3 = Group([std9, std10, std11])
        grouping = Grouping()
        grouping.add_group(group1)
        grouping.add_group(group2)
        grouping.add_group(group3)
        assert pytest.approx(survey.score_grouping(grouping)) == (72/2 + 160/3/2 + (560/15+20)/2)/3

###############################################################################
# Task 10 Test cases
###############################################################################
class TestAlphaGrouper:

    def test_make_grouping_group_size_2(self) -> None:
        grouper = AlphaGrouper(2)
        std1 = Student(1, 'Kevin')
        std2 = Student(2, 'James')
        std3 = Student(3, 'Baston')
        std4 = Student(4, 'Anthony')
        std5 = Student(5, 'Janos')
        std6 = Student(6, 'Eric')
        course = Course('CSC148')
        course.enroll_students([std1, std2, std3, std4, std5, std6])
        survey = Survey([])
        grouping = grouper.make_grouping(course, survey)
        group1 = [std4, std3]
        group2 = [std6, std2]
        group3 = [std5, std1]
        assert grouping.get_groups()[0].get_members() == group1
        assert grouping.get_groups()[1].get_members() == group2
        assert grouping.get_groups()[2].get_members() == group3

    def test_make_grouping_group_size_3(self) -> None:
        grouper = AlphaGrouper(3)
        std1 = Student(1, 'Kevin')
        std2 = Student(2, 'James')
        std3 = Student(3, 'Baston')
        std4 = Student(4, 'Anthony')
        std5 = Student(5, 'Janos')
        course = Course('CSC148')
        course.enroll_students([std1, std2, std3, std4, std5])
        survey = Survey([])
        grouping = grouper.make_grouping(course, survey)
        group1 = [std4, std3, std2]
        group2 = [std5, std1]
        assert grouping.get_groups()[0].get_members() == group1
        assert grouping.get_groups()[1].get_members() == group2


class TestGreedyGrouper:

    def test_make_grouping(self) -> None:
        grouper = GreedyGrouper(2)
        question = YesNoQuestion(1, 'True or False:')
        survey = Survey([question])
        std1 = Student(1, 'Kevin')
        answer1 = Answer(True)
        std1.set_answer(question, answer1)
        std2 = Student(2, 'James')
        answer2 = Answer(True)
        std2.set_answer(question, answer2)
        std3 = Student(3, 'Baston')
        answer3 = Answer(True)
        std3.set_answer(question, answer3)
        std4 = Student(4, 'Anthony')
        answer4 = Answer('great')
        std4.set_answer(question, answer4)
        std5 = Student(5, 'Janos')
        answer5 = Answer('nice')
        std5.set_answer(question, answer5)
        std6 = Student(6, 'Eric')
        answer6 = Answer([])
        std6.set_answer(question, answer6)
        course = Course('CSC148')
        course.enroll_students([std1, std2, std3, std4, std5, std6])
        grouping = grouper.make_grouping(course, survey)
        group1 = [std1, std2]
        group2 = [std3, std4]
        group3 = [std5, std6]
        assert grouping.get_groups()[0].get_members() == group1
        assert grouping.get_groups()[1].get_members() == group2
        assert grouping.get_groups()[2].get_members() == group3


if __name__ == '__main__':
    import pytest
    pytest.main(['tests.py', "--capture=sys", "-W", "ignore:Module already imported:pytest.PytestWarning"])
