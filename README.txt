IMPORTANT: Always make sure that your terminal is activate (env) 
           and in the same directory of this project
           Ex. (env) C:\...\...\UTS> 

Activate (env): env\Scripts\activate

How to run web program:
    1. Turn on your PHPMyAdmin database server (for this project, we do it in WAMPSERVER64)
    2. First, you need to create database named "debt_database" (based on db.py line 14)
       Just let it empty (don't create any table inside, just create database)
    3. Second, create table in terminal (open terminal with the same directory of this project)
        1. flask shell
        2. >>> from app import db
        3. >>> db.create_all()
        4. >>> quit()
    4. Third, on terminal, to able to open the website project, there are 3 ways:
        1. flask run (basic run flask)
        2. flask --debug run (run flask for development/for debugging)
        3. flask run --host="<your_ip_address>" (this run is to make the website visible
           and can be accessed by other devices with the same network connection)
        4. flask run --port=<choose the port you want, usually it's = 5000> (run flask for custom port)

        Finally, you can combine all of them
        5. flask --debug run --host="<your_ip_address>" --port=<port you want, usually it's = 5000'>
    5. Fourth, this is important to make your website visible and can be accessed by other devices.
       Check here: https://www.devopinion.com/access-localhost-from-another-computer-on-the-same-network/
    6. Finally, you can run your website application by opening the 
       Usually, it's show like this in your terminal after run it
       http://127.0.0.1:5000
       http://10.252.246.225:5000
       Just open it in your browser

Enjoy our Debt App :)
