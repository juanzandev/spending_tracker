overallDescription = """Meet the Syntax Society Team!"""

# Nolan is a first year undergraduate student from Kentucky, focusing in software and hardware engineering.

# J from Argentina: J is a computer science student from Buenos Aires with interests in software development and cybersecurity, who loves tango, football, and Argentine cuisine.

# D from Chicago: D is a computer science student focused on data science and cloud computing, who enjoys Chicago's cultural scene, live music, and deep-dish pizza."""

# (do this later)


juanDescription = """
<h3>Juan Zanguitu</h3>

<h6>Third Year CS Student</h6>

jzanguitu@hawk.iit.edu
"""

destinyDescription = """
<h3>Destiny Medina</h3>

<h6>Third Year CS Student</h6>

dmedina8@hawk.iit.edu
"""

nolanDescription = """
<h3>Nolan Lawrence</h3>

<h6>First Year CS Student</h6>

nlawrence1@hawk.iit.edu
"""


def pieChartDescription(totalSpending, totalBudget, moneyLeft):
    return f"""
<h2>Welcome to Spending Analyzer!</h2>

<h4>Here you can see a summary of your transactions over the past month, and how they effect your overall budget.</h4>


Your budget is \${totalBudget}.

You spent \${totalSpending}.

You currently have \${moneyLeft} dollars left to spend this month.


<h5>Congratulations! You are on track to increasing your spending score this month! </h5>
"""
