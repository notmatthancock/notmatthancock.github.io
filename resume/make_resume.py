import pyresume as rs

name = rs.Name(first="Matthew", middle="C.", last="Hancock")

addr = rs.Address(street="317 Mabry St. Apt 1021",
                  city="Tallahassee", state="FL", zipcode="32304")

contact = rs.Contact(name=name,
                     phone="810.656.0561",
                     email="mhancock743@gmail.com",
                     website="http://www.math.fsu.edu/~mhancock/",
                     address=addr)

edu1 = rs.EduItem(school="Florida State University", dates="Fall 2012-present",
                  degree="Ph.D. Candidate",
                  field="Applied and Computational Mathematics",
                  coursework=["Numerical Methods for Interpolation, Integration, ODEs/PDEs, Linear Algebra, and Optimization",
                              "Machine Learning",
                              "Probability theory and Statistical Inference"],
                  focus="Machine learning and image-processing methods for lung analysis"
                                    )
edu2 = rs.EduItem(school="Ferris State University", dates="Spring 2012",
                  degree="B.S.",
                  field="Applied Mathematics with Computer Science focus")

edusec = rs.Section(title="Education", items=[edu1, edu2])

wk1 = rs.WorkItem(company="Florida State University",
                  title="Teaching Assistant",
                  dates="Fall 2012-present",
                  duties=["Teaching assistant for Foundations of Computational Math (graduate level course) (Fall 2016 and Spring 2017).",
                          "Instructor for C++ computing seminar (Fall 2016).",
                          "Instructor for Calculus 1 (Spring 2016 and Summer 2016).",
                          "Instructor for Precalculus (Fall 2014 and Spring 2015).",
                          "Recitation instructor for Discrete Mathematics (Fall 2015).",
                          "Assistant with lower-level math courses (College algebra, Liberal Arts math, Trigonometry, Business calculus)."])

wk2 = rs.WorkItem(company="Occupational Research and Assessment",
                  title="Web developer",
                  dates="Fall 2011-Fall 2012",
                  duties=["Created and helped to design web systems for a number of third-party organizations using Ruby.",
                          "Learned basic web development skills."])

worksec = rs.Section(title="Work Experience", items=[wk1, wk2])

pub1 = rs.PubItem(authors=["Matthew C. Hancock", "Jerry F. Magnan"],
                  title="Lung nodule malignancy classification using only radiologist quantified image features as inputs to statistical learning algorithms: probing the Lung Image Database Consortium dataset with two statistical learning methods",
                  publication="SPIE Journal of Medical Imaging",
                  date="Dec. 2016",
                  link="http://dx.doi.org/10.1117/1.JMI.3.4.044504")

journalpubsec = rs.Section(title="Journal Publications", items=[pub1])

pub2 = rs.PubItem(authors=["Matthew C. Hancock", "Jerry F. Magnan"],
                  title="Predictive capabilities of statistical learning methods for lung nodule malignancy classification using diagnostic image features: an investigation using the Lung Image Database Consortium dataset",
                  publication="SPIE Medical Imaging Symposium, Computer-Aided Diagnosis Conference", date="Feb 2017")
confpubsec = rs.Section(title="Conference Proceedings", items=[pub2])

cskills = [
    "Python (NumPy, SciPy, Scikit Learn, Scikit Image, Theano, Cython)",
    "C++",
    "LaTeX",
    "Web (HTML, CSS, JavaScript; lesser: Ruby, PHP)",
    "SQLite, MySQL"
]
compskills = rs.Section(title="Computer skills", items=[rs.MiscItem(thing=s) for s in cskills])

resume = rs.Resume(name, contact, sections=[edusec, journalpubsec, confpubsec, worksec, compskills])

print resume.export(ttype="html", tname="basic")
