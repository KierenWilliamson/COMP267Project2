USE Comp267;

-- Creating the department table
CREATE TABLE department(
department_id int primary key auto_increment,
name varchar(100) unique not null,
description text
);
-- Adding values to department
INSERT INTO department (name, description) VALUES
('Public Works', 'Responsible for maintenance of roads, bridges, public buildings, utilities, and infrastructure.'),
('Parks and Recreation', 'Manages parks, recreational facilities, programs, trails, and community events.'),
('Police Department', 'Provides law enforcement, crime prevention, and public safety services.'),
('Fire Department', 'Handles fire suppression, emergency medical response, and disaster mitigation.'),
('Planning and Zoning', 'Regulates land use, building codes, zoning, and urban planning.'),
('Transportation', 'Oversees public transit systems, traffic management, and transportation planning.'),
('Health Department', 'Provides public health services, clinics, inspections, disease control, and health education.'),
('Finance Department', 'Handles budgeting, accounting, payroll, purchasing, and financial planning.'),
('Human Resources', 'Manages hiring, training, benefits, compliance, and employee relations.'),
('Environmental Services', 'Oversees environmental protection, waste management, and sustainability programs.'),
('Economic Development', 'Promotes business growth, tourism, community development, and job creation.'),
('Emergency Management', 'Coordinates disaster preparedness, response, and recovery operations.'),
('Housing and Community Services', 'Handles affordable housing, grants, community programs, and social services.'),
('Information Technology', 'Manages IT systems, cybersecurity, networks, and technical support.'),
('Clerk’s Office', 'Maintains public records, vital records, meeting minutes, and legal documentation.'),
('Assessor’s Office', 'Assesses property values for tax purposes.'),
('Treasurer’s Office', 'Manages tax collection, revenue distribution, and public funds.'),
('Utilities Department', 'Manages water, wastewater, electricity, and other city utilities.'),
('Animal Services', 'Oversees animal control, shelters, licensing, and public education.'),
('Legal Department', 'Provides legal counsel, handles litigation, and drafts ordinances and contracts.');


CREATE TABLE district(
district_id int primary key auto_increment,
name varchar(100) unique not null,
description text
);

CREATE TABLE topic(
topic_id int primary key auto_increment,
name varchar(100) unique not null,
description text
);

INSERT INTO topic (name, description)
VALUES
('Public Services', 'Information about services provided by government agencies, including permits, licenses, and public assistance.'),
('Taxation', 'Topics related to income tax, property tax, filing procedures, and tax policies.'),
('Healthcare Services', 'Government health programs, medical assistance, insurance plans, and public health updates.'),
('Education & Schools', 'Information about public schools, education programs, scholarships, and curriculum standards.'),
('Transportation & Infrastructure', 'Road conditions, public transportation, construction projects, and infrastructure planning.'),
('Emergency Services', 'Police, fire, rescue, disaster response, and emergency preparedness guidelines.'),
('Laws & Regulations', 'Legal codes, compliance requirements, and regulatory updates from government authorities.'),
('Elections & Voting', 'Voter registration, election dates, polling stations, and electoral processes.'),
('Environmental Protection', 'Conservation efforts, recycling programs, environmental laws, and sustainability initiatives.'),
('Social Welfare Programs', 'Assistance programs for families, housing, elderly support, and community welfare.'),
('Business & Commerce', 'Business registration, permits, regulations, and government support for enterprises.'),
('Citizen Feedback', 'Public consultations, complaints, suggestions, and feedback channels for government services.');

INSERT INTO topic (name, description)
VALUES
-- Identity & Authentication
('Digital ID Registration', 'Online service for issuing and managing digital identification credentials.'),
('eSignature Services', 'Apply, renew, and validate electronic signatures for official transactions.'),
('Account Verification Services', 'Identity verification steps using biometrics, SMS OTP, or document uploads.'),

-- Citizen Records & Certificates
('Online Birth Certificate Request', 'Submit and track electronic birth certificate applications.'),
('Marriage Certificate eService', 'Digital processing of marriage certificate applications and verification.'),
('Death Certificate Issuance Portal', 'Online request and delivery of death certificate documents.'),
('Civil Status Record Updates', 'Submit online updates for personal civil status records.'),

-- Taxes & Finance
('Online Tax Filing', 'File income, business, or property taxes electronically.'),
('Digital Tax Payments', 'Make tax payments using online banking, cards, or government payment gateways.'),
('eReceipt Validation', 'Verify authenticity of electronically issued tax receipts.'),

-- Licensing & Permits
('Driver’s License Renewal Online', 'Apply or renew a driver’s license through an online portal.'),
('Business Permit eApplication', 'Submit business permit applications and check approval status.'),
('Building Permit Online Submission', 'Upload plans, pay fees, and track approval for construction permits.'),
('Professional License Services', 'Renewal and verification of professional licenses through e-services.'),

-- Social Services & Benefits
('Social Aid Application Portal', 'Apply for financial assistance, subsidies, or social welfare benefits online.'),
('Pension Services Online', 'View contributions, request pension claims, and manage retirement benefits.'),
('Disability Assistance eService', 'Submit disability benefit applications and check eligibility digitally.'),

-- Immigration & Travel
('Visa Application Online Portal', 'Apply for visas, upload documents, and track status electronically.'),
('ePassport Appointment Scheduling', 'Book or manage passport application appointments online.'),
('Residency Permit Renewal Online', 'Submit residency renewals, pay fees, and upload documentation.'),

-- Healthcare & Public Health
('Health Insurance eEnrollment', 'Register for public health insurance programs online.'),
('Vaccination Certificate Download', 'Download or verify digital vaccination certificates.'),
('Medical Appointments eBooking', 'Schedule government hospital or clinic appointments electronically.'),

-- Legal & Justice Services
('Court Case Status Portal', 'Search and track the status of court cases online.'),
('Online Fine Payment', 'Pay traffic fines, penalties, or administrative fees electronically.'),
('Citizen Complaint eFiling', 'Submit formal complaints, disputes, or legal requests digitally.'),

-- Elections & Civic Participation
('Voter Registration Online', 'Register to vote or update voter information via digital services.'),
('Polling Location Lookup', 'Find official polling stations using an online search tool.'),
('Public Consultation ePlatform', 'Submit opinions on draft laws, regulations, or policies through an online portal.'),

-- Infrastructure & Utilities
('Water Bill Online Payment', 'Check balances and pay water utility bills electronically.'),
('Electricity Service Requests', 'Submit online requests for connection, disconnection, or meter checking.'),
('Municipal Service Tickets', 'File service tickets for waste collection, road repair, or public facility issues.')
;



CREATE TABLE gov_website (
    website_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    url VARCHAR(255) NOT NULL,
    department_id INT,
    district_id INT,         
    topic_id INT,            
    FOREIGN KEY (department_id) REFERENCES department(department_id),
    FOREIGN KEY (district_id) REFERENCES district(district_id),
    FOREIGN KEY (topic_id) REFERENCES topic(topic_id)
) ENGINE=InnoDB;


-- Example INSERTs for gov_website table

INSERT INTO gov_website (name, url, department_id) VALUES
('Guilford County Home Page', 'https://www.guilfordcountync.gov/home-page', 15), -- Clerk’s Office (general records)

('Guilford County Animal Services', 'https://www.guilfordcountync.gov/our-county/animal-services', 19),

('Guilford County Planning & Development', 'https://www.guilfordcountync.gov/government/departments-and-agencies/planning-and-development', 5),

('Guilford County Parks & Recreation', 'https://www.guilfordcountync.gov/government/departments-and-agencies/county-parks', 2),

('Guilford County Budget & Management', 'https://www.guilfordcountync.gov/departments_agencies', 8),

('Guilford County Parks Master Plan', 'https://www.guilfordcountync.gov/government/countywide-programs-and-initiatives/parks-master-plan', 2);

-- Identity & Authentication
INSERT INTO gov_website (name, url, department_id) VALUES
('NC MyNCID Identity Verification', 'https://www.ncdot.gov/dmv/offices-services/online/Pages/myncid-identity-verification.aspx', 14),
('NCID Registration & User Guide', 'https://it.nc.gov/ncid-user-guide-individual-business-users', 14),

-- Licensing & Permits (Driver ID Renewal)
('NCDMV Driver License / ID Renewal Online', 'https://www.ncdot.gov/dmv/license-id/renewal-replacement/Pages/license-renewal.aspx', 6),

-- Citizen Records & Certificates
('Guilford County Vital Records – Birth, Death & Marriage Certificates', 'https://www.guilfordcountync.gov/government/register-deeds/vital-records', 15),
('Guilford County Death Certificate Request', 'https://www.guilfordcountync.gov/government/register-deeds/vital-records/death-certificates', 15),

-- Elections & Civic Participation
('NCDMV Online Voter Registration Application', 'https://www.ncdot.gov/dmv/offices-services/online/Pages/voter-registration-application.aspx', 6),
('How to Register to Vote – N.C. State Board of Elections', 'https://www.ncsbe.gov/registering/how-register', 15),

-- Taxes & Finance
('Guilford County Online Tax Services', 'https://www.guilfordcountync.gov/business/online-tax-services', 17),

-- Identity resolution / IT
('NC eLink Statewide Entity Resolution Tool', 'https://it.nc.gov/programs/nc-government-data-analytics-center/gdac-services/nc-elink', 14);

-- Guilford County Websites
UPDATE gov_website
SET topic_id = 1
WHERE name = 'Guilford County Home Page';  -- Public Services

UPDATE gov_website
SET topic_id = 10
WHERE name = 'Guilford County Animal Services';  -- Social Welfare Programs

UPDATE gov_website
SET topic_id = 5
WHERE name = 'Guilford County Planning & Development';  -- Transportation & Infrastructure

UPDATE gov_website
SET topic_id = 1
WHERE name = 'Guilford County Parks & Recreation';  -- Public Services

UPDATE gov_website
SET topic_id = 2
WHERE name = 'Guilford County Budget & Management';  -- Taxation

UPDATE gov_website
SET topic_id = 5
WHERE name = 'Guilford County Parks Master Plan';  -- Transportation & Infrastructure


DELETE FROM gov_website
WHERE name = 'Guilford County Parks Master Plan';

UPDATE gov_website
SET topic_id = NULL
WHERE topic_id NOT IN (SELECT topic_id FROM topic);

