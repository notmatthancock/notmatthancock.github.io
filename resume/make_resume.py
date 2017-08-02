# -*- coding: utf-8 -*-

import pyresume as rs

name = rs.Name(first="Matthew", middle="C.", last="Hancock")

addr = rs.Address(street="317 Mabry St. Apt 1021",
                  city="Tallahassee", state="FL", zipcode="32304")

contact = rs.Contact(name=name,
                     phone="810.656.0561",
                     #email="mhancock743@gmail.com",
                     email="mhancock@math.fsu.edu",
                     website="https://notmatthancock.github.io",
                     address=addr)

edu1 = rs.EduItem(school="Florida State University",
                  location="Tallahasse, FL",
                  dates="Fall 2012-Fall 2017 (anticipated)",
                  degree="Ph.D. Candidate",
                  field="Applied and Computational Mathematics",
                  coursework=["Numerical Methods (interpolation, integration, ODEs/PDEs, linear algebra, and optimization)",
                              "Machine Learning",
                              "Probability theory and Statistical Inference"],
                  focus="Machine learning and image-processing methods for lung image analysis"
                                    )
edu2 = rs.EduItem(school="Ferris State University",
                  location="Big Rapids, MI",
                  dates="Spring 2012",
                  degree="B.S.",
                  field="Applied Mathematics with Computer Science focus")

edusec = rs.Section(title="Education", items=[edu1, edu2])

wk1 = rs.WorkItem(company="Florida State University",
                  location="Tallahassee, FL",
                  title="Teaching Assistant",
                  dates="Fall 2012-present",
                  duties=["Instructor, Multi-variable Calculus (Summer 2017)",
                          "Distinguished Teaching Assistant Award (2017)",
                          "Assistant, Foundations of Computational Math (graduate level course) (Fall 2016, Spring 2017).",
                          "Instructor, C++ computing seminar (Fall 2016).",
                          "Instructor, Single-variable Calculus (Spring 2016, Summer 2016).",
                          "Instructor, Precalculus (Fall 2014, Spring 2015).",
                          "Recitation instructor, Discrete Mathematics (Fall 2015).",
                          "Assistant, various math courses (College algebra, Liberal Arts math, Trigonometry, Business calculus)."])

wk2 = rs.WorkItem(company="Occupational Research and Assessment",
                  location="Big Rapids, MI",
                  title="Web developer",
                  dates="Fall 2011-Fall 2012",
                  duties=["Created and designed web systems for a number of third-party organizations using the Ruby on Rails web development framework."])

wk3 = rs.WorkItem(company="Ferris State University",
                  location="Big Rapids, MI",
                  title="Programming Tutor",
                  dates="Fall 2009-Fall 2011",
                  duties=["Tutor for undergraduate introductory programming course taught with the Python programming language."])

wk4 = rs.WorkItem(company="Ferris State University",
                  location="Big Rapids, MI",
                  title="Calculus Tutor",
                  dates="Spring 2010-Fall 2010",
                  duties=["Tutor for undergraduate calculus courses (mostly single-variable calculus material)."])

worksec = rs.Section(title="Work", items=[wk1, wk2, wk3, wk4])

pub1 = rs.PubItem(authors=["Matthew C. Hancock", "Jerry F. Magnan"],
                  title="Lung nodule malignancy classification using only radiologist quantified image features as inputs to statistical learning algorithms: probing the Lung Image Database Consortium dataset with two statistical learning methods",
                  publication="SPIE Journal of Medical Imaging",
                  date="Dec. 2016",
                  link="http://dx.doi.org/10.1117/1.JMI.3.4.044504")

journalpubsec = rs.Section(title="Journal Publications", items=[pub1])

pub2 = rs.PubItem(authors=["Matthew C. Hancock", "Jerry F. Magnan"],
                  title="Predictive capabilities of statistical learning methods for lung nodule malignancy classification using diagnostic image features: an investigation using the Lung Image Database Consortium dataset",
                  publication="SPIE Medical Imaging Symposium, Computer-Aided Diagnosis Conference (Orlando, FL)",
                  link="http://dx.doi.org/10.1117/12.2254446",
                  date="Feb. 2017")
confpubsec = rs.Section(title="Conference Proceedings", items=[pub2])

siam_seas_2017 = rs.PubItem(authors=["Matthew C. Hancock", "Jerry F. Magnan"],
                            title="Lung nodule malignancy classification using diagnostic image features",
                            publication="SIAM SEAS Conference (Tallahassee, FL)",
                            link="http://notmatthancock.github.io/research/pdf/siam-seas-2017.pdf",
                            date="Spring 2017")
postersec = rs.Section(title="Posters Presented", items=[siam_seas_2017])


pub3 = rs.PubItem(authors=["Matthew C. Hancock", "Jerry F. Magnan"],
                  title="Predictive capabilities of statistical learning methods for lung nodule malignancy classification using diagnostic image features: an investigation using the Lung Image Database Consortium dataset",
                  publication="SPIE Medical Imaging Symposium, Computer-Aided Diagnosis Conference (Orlando, FL)",
                  link="http://notmatthancock.github.io/research/talks/spieconf2017.pdf",
                  date="Feb. 2017",
                  comment="talk associated with corresponding conference proceeding")

pub4 = rs.PubItem(authors=["Matthew C. Hancock"],
                  title="10 FREE Python Libraries that will TOTALLY SHOCK you",
                  publication="FSU Math Department Graduate Student Seminar",
                  date="Spring 2017",
                  link="http://notmatthancock.github.io/research/talks/gss-python/",
                  comment="Presentation of various Python library for scientific computing. The title is a spoof on clickbait journalism.")

pub5 = rs.PubItem(authors=["Matthew C. Hancock"],
                  title="A survey a of PDE-based methods for image segmentation ",
                  publication="FSU Math Department Graduate Student Seminar",
                  date="Spring 2016",
                  link="http://notmatthancock.github.io/research/talks/gss-pdes/")

talkpubsec = rs.Section(title="Talks Given", items=[pub3, pub4, pub5])

cskills = [
    "High-level programming languages: Python (NumPy, SciPy, Scikit Learn, Scikit Image, Theano, Cython), JavaScript, Ruby, PHP",
    "Mid-level programming languages: C++, Fortran",
    "Markup languages: LaTeX, Web (HTML, CSS)",
    "Relational databases languages: SQLite, MySQL",
    "General Unix-like operating system tools"
]
compskills = rs.Section(title="Computational Fluency", items=[rs.MiscItem(text=s) for s in cskills])

miscsec = rs.Section(title="Activities", items=[
    rs.MiscItem(
        title="Participant in Capital One modeling competition",
        text=("Our group created a neural network model for identifying "
              "fraudulent credit card transactions. This involved "
              "preprocessing tens of gigabytes of raw data to be placed "
              "into an SQL database, whereafter a custom, GPU-based "
              "neural network was trained.")
    ),
    rs.MiscItem(
        title="Creator and developer of Pylidc",
        text=("Pylidc is a software library for working with LIDC "
              "lung CT dataset. The library is built with Python and its "
              "associated scientific computing libraries and is "
              "freely available."),
        link="https://github.com/pylidc/pylidc."
    ),
    rs.MiscItem(
        title="C++ and Fortran Reference Guides for Graduate Seminar",
        text=("In collaboration with a fellow graduate student, Emacs "
              "Org-mode was used to create C++ and Fortran reference "
              "guides to be used in the Applied and Computational "
              "Mathematics computational seminar for first year graduate "
              "students at FSU. The guides are available under a "
              "Creative Commons license."),
        link="http://notmatthancock.github.io/teaching/acm-computing-seminar/resources/langs/cpp/"
    )
])

#resume = rs.Resume(name, contact, sections=[edusec, journalpubsec, confpubsec, worksec, compskills])
resume = rs.Resume(name, contact, sections=[edusec, worksec, compskills, miscsec,
                                            journalpubsec, confpubsec, talkpubsec,
                                            postersec])

print resume.export(ttype="latex", tname="basic")
