import streamlit as st
import requests
from PIL import Image
import os
import mysql
import mysql.connector
from datetime import date, datetime
import webbrowser
import smtplib, ssl
from email.message import EmailMessage

def change_page(page):
    st.session_state.page = page
    print(page)

def change_session_state(state, i):
    if st.session_state[state] >= i:
        return
    st.session_state[state] = i
    print(f"{state} = {i}")
    
def debug_button():
    st.session_state.page = "upcoming_lesson"
    st.session_state.student_id = 1
    st.session_state.login_date = date.today().strftime("%B %d, %Y")
    st.session_state.login_time = datetime.now().strftime("%H:%M:%S")

def open_url(url):
    webbrowser.open_new_tab(url)
    
def get_day(n):
    if n == 1:
        return "Mon"
    elif n == 2:
        return "Tue"
    elif n == 3:
        return "Wed"
    elif n == 4:
        return "Thu"
    elif n == 5:
        return "Fri"
def get_time(time):
    return time[0:-2]

def send_email(materials, email):
    password = "12348765AbC"
    
    sender = "courseflowcoursematerial@gmail.com"
    receiver = email
    subject = "Coures Material From CourseFlow"
    body = "This message was sent automatically."
    for item in materials:
        body += "\n" + f"{item[0]}" + "\n" + f"{item[1]}"
    
    em = EmailMessage()
    em['From'] = sender
    em['To'] = receiver
    em['Subject'] = subject
    em.set_content(body)
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login('courseflowcoursematerial@gmail.com', password)
        smtp.sendmail(sender, receiver, em.as_string())
        smtp.quit()

def print_course(lecture_list, day, time):
    for item in lecture_list:
        name = item[0]
        weekday = item[2]
        start = int(f"{item[3]}".split(':')[0])
        end = int(f"{item[4]}".split(':')[0])
        if weekday == day and time > start and time <= end:
            if time == start + 1:
                st.button(name, key=name+str(weekday), disabled=True, use_container_width=True)
            else:
                st.button("", key=name+str(weekday)+str(time), disabled=True, use_container_width=True)
    return
    
def display_timetable(lecture_list):
    st.title("Timetable")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col2:
        st.subheader("Mon")
    with col3:
        st.subheader("Tue")
    with col4:
        st.subheader("Wed")
    with col5:
        st.subheader("Thu")
    with col6:
        st.subheader("Fri")

    for i in range(12):
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.write(f"{i+8}:00")
        with col2:
            print_course(lecture_list, 1, i+8)
        with col3:
            print_course(lecture_list, 2, i+8)
        with col4:
            print_course(lecture_list, 3, i+8)
        with col5:
            print_course(lecture_list, 4, i+8)
        with col6:
            print_course(lecture_list, 5, i+8)
    return

def login_gui():
    if "gui" not in st.session_state:
        st.session_state.gui = 0
    image = Image.open(os.path.join("image", "Icon.png"))
    st.image(image, width=500)
    st.title("CourseFlow")
    st.subheader("Welcome Back!")
    st.button("Login", on_click=change_session_state, args=["gui", 1])
    st.button("Debug", on_click=debug_button)
    if st.session_state.gui < 1:
        return
    # login system (need to be implemented)
    result = requests.get("http://127.0.01:5000/login").json()
    if result["login"] == "Y":
        st.session_state.page = "upcoming_lesson"
        st.session_state.login_date = date.today().strftime("%B %d, %Y")
        st.session_state.login_time = datetime.now().strftime("%H:%M:%S")
        page()
    else:
        return
    return
        
def page():
    myconn = mysql.connector.connect(host="localhost", user="root", passwd="20011013", database="facerecognition")
    cursor = myconn.cursor()
    st.session_state.cursor = cursor
    if st.session_state.page != "course_information":
        st.title("Welcome Back!")
        st.write(date.today().strftime("%B %d, %Y"))
    sb = st.sidebar
    with sb:
        image = Image.open(os.path.join("image", "Icon.png"))
        st.image(image, width=200)
        cursor.execute(f"SELECT name, cirriculum FROM Student WHERE student_id = {st.session_state.student_id}")
        result = cursor.fetchall()
        st.write(result[0][0])
        st.write(result[0][1])
        st.title("DashBoard")
        st.button("Upcoming Lesson", on_click=change_page, args=["upcoming_lesson"])
        st.button("Timetable", on_click=change_page, args=["timetable"])
        st.button("Course List", on_click=change_page, args=["course_list"])
        st.write("###")
        st.write("###")
        st.write("###")
        st.write("###")
        st.write("Login Time:")
        st.write(f"{st.session_state.login_date}")
        st.write(f"{st.session_state.login_time}")
        st.button("Logout", on_click=change_session_state, args=["page", "login"])
    # Upcoming Lesson Page/ Home Page
    if st.session_state.page == "upcoming_lesson":
        cursor.execute(f"SELECT class_id, course_id FROM Enroll WHERE student_id = {st.session_state.student_id}")
        course_list = cursor.fetchall()
        cursor.execute(f"\
            SELECT L.course_id, L.class_id, L.start_time, L.end_time, L.venue_id \
            FROM Lecture L NATURAL JOIN (\
            SELECT class_id, course_id FROM Enroll WHERE student_id = {st.session_state.student_id}) as T1 \
            WHERE L.start_time BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 1 HOUR) \
            AND L.weekday = {datetime.now().weekday() + 1}")
        upcoming_lesson_list = cursor.fetchall()
        
        # no upcoming lesson
        if upcoming_lesson_list == []:
            st.subheader("No upcoming lesson with in the next hour.")
            cursor.execute(f"\
                SELECT L.course_id, L.class_id, L.weekday, L.start_time, L.end_time \
                FROM Lecture L NATURAL JOIN (\
                SELECT class_id, course_id FROM Enroll WHERE student_id = {st.session_state.student_id}) as T1\
            ")
            lecture_list = cursor.fetchall()
            display_timetable(lecture_list)
        
        # have upcoming lesson
        else:
            # debug
            #
            st.subheader(f"Course Code: {upcoming_lesson_list[0][0]}")
            st.subheader(f"Start Time: {upcoming_lesson_list[0][2]}")
            container = st.container()
            with container:
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Classroom Location:")
                with col2:
                    cursor.execute(f"SELECT location FROM Venue WHERE venue_id = {upcoming_lesson_list[0][4]}")
                    result = cursor.fetchall()
                    st.subheader(f"{result[0][0]}")
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Lecturer:")
                with col2:
                    cursor.execute(f"SELECT instructor_id FROM Teach \
                                    WHERE class_id = '{upcoming_lesson_list[0][1]}' AND course_id = '{upcoming_lesson_list[0][0]}'")
                    result = cursor.fetchall()
                    cursor.execute(f"SELECT name from Instructor WHERE instructor_id = '{result[0][0]}'")
                    result = cursor.fetchall()
                    st.subheader(result[0])
                st.subheader("Teacher's Message")
                cursor.execute(f"SELECT message FROM TeacherMessage\
                                WHERE class_id = '{upcoming_lesson_list[0][1]}' AND course_id = '{upcoming_lesson_list[0][0]}'")
                result = cursor.fetchall()
                st.write(result[0][0])
                cursor.execute(f"SELECT name, link FROM Material \
                                 WHERE class_id = '{upcoming_lesson_list[0][1]}' AND course_id = '{upcoming_lesson_list[0][0]}'")
                materials = cursor.fetchall()
                st.subheader("Course Materials")
                # no course material
                if len(materials) == 0:
                    st.write("No course material available.")
                # have course material
                else:
                    for item in materials:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(item[0])
                        with col2:
                            st.button("Download", on_click=open_url, args=[item[1]])
                    cursor.execute(f"SELECT email FROM Student WHERE student_id = '{st.session_state.student_id}'")
                    email = cursor.fetchall()[0]
                    st.button("Send Course Material to Email", on_click=send_email, args=[materials, email])
    # Timetable Page
    elif st.session_state.page == "timetable":
        cursor.execute(f"\
            SELECT L.course_id, L.class_id, L.weekday, L.start_time, L.end_time \
            FROM Lecture L NATURAL JOIN (\
            SELECT class_id, course_id FROM Enroll WHERE student_id = {st.session_state.student_id}) as T1\
            ")
        lecture_list = cursor.fetchall()
        display_timetable(lecture_list)
        return
    # Course List Page
    elif st.session_state.page == "course_list":
        def course_information_page(course, department, instructor, instructor_dept, message, materials, email):
            # class_id, course_id, name, dept_id
            st.session_state.page = "course_information"
            st.title("Course Information")
            st.subheader(course[2])
            st.write(f"Department: '{department}'")
            st.subheader("Instructor Details")
            st.subheader("\t"+instructor[0])
            st.write(f"Department: {instructor_dept}")
            st.write(f"Email: {instructor[2]}")
            st.write(f"Office: {instructor[3]}")
            st.write(f"Office Hours: {get_day(instructor[6])} {get_time(str(instructor[4]))}-{get_time(str(instructor[5]))}")
            st.subheader("Teacher's Message")
            st.write(message)
            st.subheader("Course Materials")
            # no course material
            if len(materials) == 0:
                st.write("No course material available.")
            # have course material
            else:
                for item in materials:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(item[0])
                    with col2:
                        st.button("Download", on_click=open_url, args=[item[1]])
                st.button("Send Course Material to Email", on_click=send_email, args=[materials, email])
        # Course List Page Layout/UI
        st.title("Course List")
        cursor.execute(f"SELECT class_id, course_id FROM Enroll WHERE student_id = '{st.session_state.student_id}'")
        course_list_temp = cursor.fetchall()
        course_list = []
        for i in range(len(course_list_temp)):
            cursor.execute(f"SELECT name, dept_id FROM Course WHERE course_id = '{course_list_temp[i][1]}'")
            result = cursor.fetchall()
            print(result)
            course_list.append([])
            course_list[i].append(course_list_temp[i][0])
            course_list[i].append(course_list_temp[i][1])
            course_list[i].append(result[0][0])
            course_list[i].append(result[0][1])
        course_buttons = []
        for course in course_list:
            cursor.execute(f"SELECT name FROM Department WHERE dept_id = '{course[3]}'")
            department = cursor.fetchall()[0][0]
            cursor.execute(f"SELECT instructor_id FROM Teach \
                             WHERE class_id = '{course[0]}' AND course_id = '{course[1]}'")
            instructor_id = cursor.fetchall()[0][0]
            cursor.execute(f"SELECT name, dept_id, email, office_location, office_hour_start, office_hour_end, office_hour_weekday \
                             FROM Instructor WHERE instructor_id = '{instructor_id}'")
            instructor = cursor.fetchall()[0]
            cursor.execute(f"SELECT name FROM Department WHERE dept_id = '{instructor[1]}'")
            instructor_dept = cursor.fetchall()[0]
            cursor.execute(f"SELECT message FROM TeacherMessage\
                             WHERE class_id = '{course[0]}' AND course_id = '{course[1]}'")
            message = cursor.fetchall()[0][0]
            cursor.execute(f"SELECT name, link FROM Material \
                             WHERE class_id = '{course[0]}' AND course_id = '{course[1]}'")
            materials = cursor.fetchall()
            cursor.execute(f"SELECT email FROM Student WHERE student_id = '{st.session_state.student_id}'")
            email = cursor.fetchall()[0]
            course_buttons.append(st.button(f"{course[1]}\t\t{course[2]}",
                                            on_click=course_information_page,
                                            args=[course, department, instructor, instructor_dept, message, materials, email],
                                            use_container_width=True))
        return

if __name__ == "__main__":
    if "page" not in st.session_state:
        login_gui()
    elif st.session_state.page == "login":
        login_gui()
    else:
        page()