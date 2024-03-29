
from DSR.utils import logger
from DSR.constants import ERROR_MSG
from .models import (
    UserAccount, PhoneNumber, CompanyProfile, Branch, Role, Address, State,
    Country)



class UserOnboarding:
    def __init__(self):
        super().__init__()

    def register_user(self, data):
        """
        Register a new user by creating a user account, setting up a user
        profile, creating a company profile, and assigning a tenant and role
        to the user.

        Args:
            data (dict): A dictionary containing the user registration data
            including email, password, first name, last name, address, phone,
            company profile, and tenant ID.

        Returns:
            tuple: A tuple containing a boolean value indicating if the user
            has been registered successfully, and a message indicating the
            result of the registration process.
        """
        try:

            email = data.get('email')
            password = data.get('password')
            company_details = data.get('company_details')
            phone_details = data.get('phone_details')
            

            if UserAccount.filter_user(email=email).exists():
                return False, "Email already registered"
            
            # country = Country.get_country(name=phone_details.get('country'))
            phone = PhoneNumber.filter_phone_number(phone=phone_details.get('phone_number')).exists()
            if phone:
                return False, "Phone number already registered."

            user = UserAccount.objects.create_user(email, password)
            if not user:
                return False, "Error creating user."

            user = self.create_user_profile(user, data)
            if not user:
                return False, "Error creating user profile."

            company_profile = self.create_company_profile(company_details)
            if not company_profile:
                return False, "Error creating company profile."

            user.company = company_profile
            user.save()

            return True, 'User has been registered successfully'
        except Exception as e:
            logger.error(
                f"UserOnBoarding | Error in register_user : {e}", exc_info=True)
            return False, ERROR_MSG

    def create_company_profile(self, company_details):
        try:
            """
            Create a company profile in the database.

            Args:
                data (dict): A dictionary containing the company profile data.
                It should include the company ID (optional), company name,
                branch, and company address.

            Returns:
                Company: The created or retrieved company object from the database.
            """
            company_id = company_details.get('company_id')
            branch = self.create_branch(company_details.get('branch_details'))

            company, created = CompanyProfile.objects.get_or_create(
                internal_id=company_id,
                defaults={
                    "name": company_details.get('name'),
                    "branch": branch
                }
            )

            return company
        except Exception as e:
            logger.error(f'Error in create_company_profile :{e}', exc_info=True)
            return None

    def create_branch(self, data):
        """
        Create a branch object in the database.

        Args:
            data (dict): A dictionary containing the branch name and address data. The branch name is a string and the branch address is a dictionary with keys 'address_1', 'address_2', 'zip_code', 'state', and 'country'.

        Returns:
            branch (Branch): The created branch object in the database.
        """
        try:
            branch_name = data.get('branch_name')
            branch_address = self.create_address(data.get('branch_address'))

            branch, created = Branch.objects.get_or_create(
                branch_name=branch_name,
                defaults={"branch_address": branch_address}
            )
            return branch
        except Exception as e:
            logger.error(f'Error in create_branch: {e}', exc_info=True)
            return None

    def create_user_profile(self, user, data):
        try:
            """
            Create a user profile by setting various attributes of the user object
            based on the provided data.

            Args:
                user (UserAccount): The user object for which the profile is being created.
                data (dict): A dictionary containing the user profile data.

            Returns:
                UserAccount: The updated user object with the profile attributes set.
            """
            from tenant.models import Tenant
            tenant = Tenant.objects.get(internal_id=data.get('tenant_id'), is_active=True)

            role = data.get('role')
            if role.get('role_id'):
                role = Role.objects.get(
                    internal_id=role.get('role_id'), tenant=tenant, is_active=True)
            else:
                role = Role.objects.create(
                    slug='owner', name='Owner', tenant=tenant)

            phone = self.create_phone(data.get('phone_details'))
            user_address = self.create_address(data.get('address'))

            user.first_name = data.get('first_name')
            user.last_name = data.get('last_name')
            user.secondary_email = data.get('secondary_email')
            user.gender = data.get('gender')
            user.dob = data.get('dob')
            user.joining_date = data.get('joining_date')
            user.address = user_address
            user.phone = phone
            user.tenant = tenant
            user.role = role
            return user
        except Exception as e:
            logger.error(f'Error in create_user_profile :{e}',exc_info=True)
            return None

    def create_address(self, address_data):
        try:
            """
            Create a new address object in the database using the provided address data.

            Args:
                address_data (dict): A dictionary containing the address data,
                including the address 1, address 2, zip code, state, and country.

            Returns:
                Address: The created address object in the database.
            """
            state = State.objects.get(name=address_data.get('state'))
            country = Country.objects.get(name=address_data.get('country'))
            address = Address.objects.create(
                address_1=address_data.get('address_1'),
                address_2=address_data.get('address_2'),
                zip_code=address_data.get('zip_code'),
                state=state,
                country=country
            )
            return address
        except Exception as e:
            logger.error(f'Error in create_address :{e}',exc_info=True)
            return None

    def create_phone(self, phone_details):
        try:
            """
            Creates a new phone number object in the database using the
            provided phone data.

            Args:
                phone_data (dict): A dictionary containing the phone data,
                including the country name and phone number.

            Returns:
                PhoneNumber: The created phone number object in the database.
            """
            country_name = phone_details.get('country')
            phone_number = phone_details.get('phone_number')
            country = Country.objects.get(name=country_name)
            phone = PhoneNumber.objects.create(phone=phone_number, country=country)
            return phone
        except Exception as e:
            logger.error(f'Error in create_phone :{e}',exc_info=True)
            return None
