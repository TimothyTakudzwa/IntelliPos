TYPE_CHOICES = (
    ('ADMIN','Adminstrator'),
    ('TELLER', 'Teller'),
    ('Supervisor', 'Supervisor')    
)
COMPANY_TYPE = (
    ('SOLE TRADER','SOLE TRADER'),
    ('PRIVATE LIMITED COMPANY', 'Private Limited Company'),
    ('PRIVATE BUSINESS Corporate', 'Private Business Corporate')    
)

create_account_email = '''
Hi {0}

Welcome to IntelliPOS. An account was created using this email for Merchant: {1}. You have been registered as the {2} of {1}.
Your Username: {3}

Please Click the Link below to set your PIN and start using IntelliPos
{4}

Kind Regards 
IntelliPOS Support Team

'''

create_account_email_user = '''
Hi {0}

Welcome to IntelliPOS. An account was created using this email for Merchant: {1}. You have been registered as the {2} of {1}.
Your Username: {3}
You IntelliPOS ID: {4}

Please user the above details and the password you set to log in to your Merchant Account

Kind Regards 
IntelliPOS Support Team

'''

INDUSTRY_CHOICES = (("Accounting", "Accounting" ), 
("Airlines / Aviation","Airlines / Aviation"),
("Alternative Dispute Resolution","Alternative Dispute Resolution"),
("Alternative Medicine","Alternative Medicine"),
("Animation","Animation"),
("Apparel / Fashion","Apparel / Fashion"),
("Architecture / Planning","Architecture / Planning"),
("Arts / Crafts","Arts / Crafts"),
("Automotive","Automotive"),
("Aviation / Aerospace","Aviation / Aerospace"),
("Banking / Mortgage","Banking / Mortgage"),
("Biotechnology / Greentech","Biotechnology / Greentech"),
("Broadcast Media","Broadcast Media"),
("Building Materials","Building Materials"),
("Business Supplies / Equipment","Business Supplies / Equipment"),
("Capital Markets / Hedge Fund / Private Equity","Capital Markets / Hedge Fund / Private Equity"),
("Chemicals","Chemicals"),
("Civic / Social Organization","Civic / Social Organization"),
("Civil Engineering","Civil Engineering"),
("Commercial Real Estate","Commercial Real Estate"),
("Computer Games","Computer Games"),
("Computer Hardware","Computer Hardware"),
("Computer Networking","Computer Networking"),
("Computer Software / Engineering","Computer Software / Engineering"),
("Computer / Network Security","Computer / Network Security"),
("Construction","Construction"),
("Consumer Electronics","Consumer Electronics"),
("Consumer Goods","Consumer Goods"),
("Consumer Services","Consumer Services"),
("Cosmetics","Cosmetics"),
("Dairy","Dairy"),
("Defense / Space","Defense / Space"),
("Design","Design"),
("E - Learning","E - Learning"),
("Education Management","Education Management"),
("Electrical / Electronic Manufacturing","Electrical / Electronic Manufacturing"),
("Entertainment / Movie Production","Entertainment / Movie Production"),
("Environmental Services","Environmental Services"),
("Events Services","Events Services"),
("Executive Office","Executive Office"),
("Facilities Services","Facilities Services"),
("Farming","Farming"),
("Financial Services","Financial Services"),
("Fine Art","Fine Art"),
("Fishery","Fishery"),
("Food Production","Food Production"),
("Food / Beverages","Food / Beverages"),
("Fundraising","Fundraising"),
("Furniture","Furniture"),
("Gambling / Casinos","Gambling / Casinos"),
("Glass / Ceramics / Concrete","Glass / Ceramics / Concrete"),
("Government Administration","Government Administration"),
("Government Relations","Government Relations"),
("Graphic Design / Web Design","Graphic Design / Web Design"),
("Health / Fitness","Health / Fitness"),
("Higher Education / Acadamia","Higher Education / Acadamia"),
("Hospital / Health Care","Hospital / Health Care"),
("Hospitality","Hospitality"),
("Human Resources / HR","Human Resources / HR"),
("Import / Export","Import / Export"),
("Individual / Family Services","Individual / Family Services"),
("Industrial Automation","Industrial Automation"),
("Information Services","Information Services"),
("Information Technology / IT","Information Technology / IT"),
("Insurance","Insurance"),
("International Affairs","International Affairs"),
("International Trade / Development","International Trade / Development"),
("Internet","Internet"),
("Investment Banking / Venture","Investment Banking / Venture"),
("Investment Management / Hedge Fund / Private Equity","Investment Management / Hedge Fund / Private Equity"),
("Judiciary","Judiciary"),
("Law Enforcement","Law Enforcement"),
("Law Practice / Law Firms","Law Practice / Law Firms"),
("Legal Services","Legal Services"),
("Legislative Office","Legislative Office"),
("Leisure / Travel","Leisure / Travel"),
("Library","Library"),
("Logistics / Procurement","Logistics / Procurement"),
("Luxury Goods / Jewelry","Luxury Goods / Jewelry"),
("Machinery","Machinery"),
("Market Research","Market Research"),
("Marketing / Advertising / Sales","Marketing / Advertising / Sales"),
("Mechanical or Industrial Engineering","Mechanical or Industrial Engineering"),
("Media Production","Media Production"),
("Medical ","Medical "),
("Military Industry","Military Industry"),
("Mining / Metals","Mining / Metals"),
("Music","Music"),
("Newspapers / Journalism","Newspapers / Journalism"),
("Non - Profit / Volunteering","Non - Profit / Volunteering"),
("Oil / Energy / Solar / Greentech","Oil / Energy / Solar / Greentech"),
("Other Industry","Other Industry"),
("Pharmaceuticals","Pharmaceuticals"),
("Political Organization","Political Organization"),
("Primary / Secondary Education","Primary / Secondary Education"),
("Printing","Printing"),
("Real Estate / Mortgage","Real Estate / Mortgage"),
("Restaurants","Restaurants"),
("Retail Industry","Retail Industry"),
("Sports","Sports"),
("Telecommunications","Telecommunications"),
("Transportation","Transportation"))
TYPE_CHOICES = (
    ('INDIVIDUAL','Individual'),
    ('S_ADMIN', 'Supplier Admin'),
    ('BUYER', 'Buyer'),
    ('SUPPLIER', 'Supplier'),
    ('SS_SUPPLIER', 'Service Station Rep'),
    
)

BANKS = (
    ("AFC", "AFC"), ("AGRIBANK", "AGRIBANK"), ("BANC ABC","BANC ABC"), ("CABS","CABS"), ("CBZ","CBZ"), ("ECOBANK","ECOBANK"), ("FBC","FBC"), ("FBC BS","FBC BS"),
    ("FIRST CAPITAL BANK","FIRST CAPITAL BANK"), ("GETBUCKS","GETBUCKS"), ("NEDBANK","NEDBANK"), ("METBANK","METBANK"), ("MFS","MFS"), ("NBS","NBS"),
    ("NMB","NMB"), ("POSB","POSB"), ("STANBIC BANK","STANBIC BANK"), ("STANDARD CHARTERED","STANDARD CHARTERED"), ("STEWARD BANK","STEWARD BANK"), ("ONEMONEY","ONEMONEY"),  ("EMPOWER BANK","EMPOWER BANK"),
    ("ZB BANK","ZB BANK")
    )

