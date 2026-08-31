class User:

    def __init__(
        self,
        user_id,
        name,
        email,
        password,
        role,
        approved=False
    ):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.approved = approved


class Course:

    def __init__(
        self,
        course_id,
        title,
        description,
        fee,
        days,
        instructor_id=""
    ):
        self.course_id = course_id
        self.title = title
        self.description = description
        self.fee = fee
        self.days = days
        self.instructor_id = instructor_id


class Enrollment:

    def __init__(
        self,
        enrollment_id,
        student_id,
        course_id,
        percentage,
        discount,
        final_fee,
        status="Pending"
    ):
        self.enrollment_id = enrollment_id
        self.student_id = student_id
        self.course_id = course_id
        self.percentage = percentage
        self.discount = discount
        self.final_fee = final_fee
        self.status = status


class Module:

    def __init__(
        self,
        module_id,
        course_id,
        title,
        description=""
    ):
        self.module_id = module_id
        self.course_id = course_id
        self.title = title
        self.description = description


class Task:

    def __init__(
        self,
        task_id,
        module_id,
        title,
        description=""
    ):
        self.task_id = task_id
        self.module_id = module_id
        self.title = title
        self.description = description


class Assignment:

    def __init__(
        self,
        assignment_id,
        course_id,
        title,
        description="",
        total_marks=100
    ):
        self.assignment_id = assignment_id
        self.course_id = course_id
        self.title = title
        self.description = description
        self.total_marks = total_marks


class Exam:

    def __init__(
        self,
        exam_id,
        course_id,
        title,
        total_marks=100
    ):
        self.exam_id = exam_id
        self.course_id = course_id
        self.title = title
        self.total_marks = total_marks


class Question:

    def __init__(
        self,
        question_id,
        exam_id,
        question,
        option_a,
        option_b,
        option_c,
        option_d,
        answer
    ):
        self.question_id = question_id
        self.exam_id = exam_id
        self.question = question
        self.option_a = option_a
        self.option_b = option_b
        self.option_c = option_c
        self.option_d = option_d
        self.answer = answer


class Attendance:

    def __init__(
        self,
        attendance_id,
        course_id,
        student_id,
        date,
        status
    ):
        self.attendance_id = attendance_id
        self.course_id = course_id
        self.student_id = student_id
        self.date = date
        self.status = status