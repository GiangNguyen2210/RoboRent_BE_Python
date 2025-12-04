from typing import Optional
import datetime
import decimal

from sqlalchemy import BigInteger, Boolean, Column, DateTime, Double, ForeignKeyConstraint, Identity, Index, Integer, Numeric, PrimaryKeyConstraint, String, Table, Text, Time
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class AspNetRoles(Base):
    __tablename__ = 'AspNetRoles'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_AspNetRoles'),
        Index('RoleNameIndex', 'NormalizedName', unique=True)
    )

    Id: Mapped[str] = mapped_column(Text, primary_key=True)
    Name: Mapped[Optional[str]] = mapped_column(String(256))
    NormalizedName: Mapped[Optional[str]] = mapped_column(String(256))
    ConcurrencyStamp: Mapped[Optional[str]] = mapped_column(Text)

    AspNetUsers: Mapped[list['AspNetUsers']] = relationship('AspNetUsers', secondary='AspNetUserRoles', back_populates='AspNetRoles_')
    AspNetRoleClaims: Mapped[list['AspNetRoleClaims']] = relationship('AspNetRoleClaims', back_populates='AspNetRoles_')


class AspNetUsers(Base):
    __tablename__ = 'AspNetUsers'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_AspNetUsers'),
        Index('EmailIndex', 'NormalizedEmail'),
        Index('UserNameIndex', 'NormalizedUserName', unique=True)
    )

    Id: Mapped[str] = mapped_column(Text, primary_key=True)
    EmailConfirmed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    PhoneNumberConfirmed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    TwoFactorEnabled: Mapped[bool] = mapped_column(Boolean, nullable=False)
    LockoutEnabled: Mapped[bool] = mapped_column(Boolean, nullable=False)
    AccessFailedCount: Mapped[int] = mapped_column(Integer, nullable=False)
    Status: Mapped[Optional[str]] = mapped_column(Text)
    UserName: Mapped[Optional[str]] = mapped_column(String(256))
    NormalizedUserName: Mapped[Optional[str]] = mapped_column(String(256))
    Email: Mapped[Optional[str]] = mapped_column(String(256))
    NormalizedEmail: Mapped[Optional[str]] = mapped_column(String(256))
    PasswordHash: Mapped[Optional[str]] = mapped_column(Text)
    SecurityStamp: Mapped[Optional[str]] = mapped_column(Text)
    ConcurrencyStamp: Mapped[Optional[str]] = mapped_column(Text)
    PhoneNumber: Mapped[Optional[str]] = mapped_column(Text)
    LockoutEnd: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    AspNetRoles_: Mapped[list['AspNetRoles']] = relationship('AspNetRoles', secondary='AspNetUserRoles', back_populates='AspNetUsers')
    Accounts: Mapped[list['Accounts']] = relationship('Accounts', back_populates='AspNetUsers_')
    AspNetUserClaims: Mapped[list['AspNetUserClaims']] = relationship('AspNetUserClaims', back_populates='AspNetUsers_')
    AspNetUserLogins: Mapped[list['AspNetUserLogins']] = relationship('AspNetUserLogins', back_populates='AspNetUsers_')
    AspNetUserTokens: Mapped[list['AspNetUserTokens']] = relationship('AspNetUserTokens', back_populates='AspNetUsers_')


class EventActivities(Base):
    __tablename__ = 'EventActivities'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_EventActivities'),
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    Name: Mapped[Optional[str]] = mapped_column(Text)
    Description: Mapped[Optional[str]] = mapped_column(Text)
    IsDeleted: Mapped[Optional[bool]] = mapped_column(Boolean)

    ActivityTypes: Mapped[list['ActivityTypes']] = relationship('ActivityTypes', back_populates='EventActivities_')
    Rentals: Mapped[list['Rentals']] = relationship('Rentals', back_populates='EventActivities_')


class RoboTypes(Base):
    __tablename__ = 'RoboTypes'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_RoboTypes'),
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    TypeName: Mapped[Optional[str]] = mapped_column(Text)
    Description: Mapped[Optional[str]] = mapped_column(Text)
    IsDeleted: Mapped[Optional[bool]] = mapped_column(Boolean)

    RobotAbilities: Mapped[list['RobotAbilities']] = relationship('RobotAbilities', back_populates='RoboTypes_')
    Robots: Mapped[list['Robots']] = relationship('Robots', back_populates='RoboTypes_')
    RobotTypeOfEvents: Mapped[list['RobotTypeOfEvents']] = relationship('RobotTypeOfEvents', back_populates='RoboTypes_')
    TypesOfRobos: Mapped[list['TypesOfRobos']] = relationship('TypesOfRobos', back_populates='RoboTypes_')
    RentalDetails: Mapped[list['RentalDetails']] = relationship('RentalDetails', back_populates='RoboTypes_')


class EFMigrationsHistory(Base):
    __tablename__ = '__EFMigrationsHistory'
    __table_args__ = (
        PrimaryKeyConstraint('MigrationId', name='PK___EFMigrationsHistory'),
    )

    MigrationId: Mapped[str] = mapped_column(String(150), primary_key=True)
    ProductVersion: Mapped[str] = mapped_column(String(32), nullable=False)


class Accounts(Base):
    __tablename__ = 'Accounts'
    __table_args__ = (
        ForeignKeyConstraint(['UserId'], ['AspNetUsers.Id'], ondelete='CASCADE', name='FK_Accounts_AspNetUsers_UserId'),
        PrimaryKeyConstraint('Id', name='PK_Accounts'),
        Index('IX_Accounts_UserId', 'UserId')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    UserId: Mapped[str] = mapped_column(Text, nullable=False)
    FullName: Mapped[Optional[str]] = mapped_column(Text)
    PhoneNumber: Mapped[Optional[str]] = mapped_column(Text)
    DateOfBirth: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    gender: Mapped[Optional[str]] = mapped_column(Text)
    IdentificationIsValidated: Mapped[Optional[bool]] = mapped_column(Boolean)
    isDeleted: Mapped[Optional[bool]] = mapped_column(Boolean)
    Status: Mapped[Optional[str]] = mapped_column(Text)

    AspNetUsers_: Mapped['AspNetUsers'] = relationship('AspNetUsers', back_populates='Accounts')
    ContractTemplates: Mapped[list['ContractTemplates']] = relationship('ContractTemplates', foreign_keys='[ContractTemplates.CreatedBy]', back_populates='Accounts_')
    ContractTemplates_: Mapped[list['ContractTemplates']] = relationship('ContractTemplates', foreign_keys='[ContractTemplates.UpdatedBy]', back_populates='Accounts1')
    FaceProfiles: Mapped[list['FaceProfiles']] = relationship('FaceProfiles', back_populates='Accounts_')
    PaymentTransactions: Mapped[list['PaymentTransactions']] = relationship('PaymentTransactions', back_populates='Accounts_')
    Rentals: Mapped[list['Rentals']] = relationship('Rentals', foreign_keys='[Rentals.AccountId]', back_populates='Accounts_')
    Rentals_: Mapped[list['Rentals']] = relationship('Rentals', foreign_keys='[Rentals.StaffId]', back_populates='Accounts1')
    ActualDeliveries: Mapped[list['ActualDeliveries']] = relationship('ActualDeliveries', back_populates='Accounts_')
    ChatRooms: Mapped[list['ChatRooms']] = relationship('ChatRooms', foreign_keys='[ChatRooms.CustomerId]', back_populates='Accounts_')
    ChatRooms_: Mapped[list['ChatRooms']] = relationship('ChatRooms', foreign_keys='[ChatRooms.StaffId]', back_populates='Accounts1')
    ContractDrafts: Mapped[list['ContractDrafts']] = relationship('ContractDrafts', foreign_keys='[ContractDrafts.ManagerId]', back_populates='Accounts_')
    ContractDrafts_: Mapped[list['ContractDrafts']] = relationship('ContractDrafts', foreign_keys='[ContractDrafts.StaffId]', back_populates='Accounts1')
    FaceVerifications: Mapped[list['FaceVerifications']] = relationship('FaceVerifications', back_populates='Accounts_')
    PriceQuotes: Mapped[list['PriceQuotes']] = relationship('PriceQuotes', back_populates='Accounts_')
    ChatMessages: Mapped[list['ChatMessages']] = relationship('ChatMessages', back_populates='Accounts_')
    CustomerContracts: Mapped[list['CustomerContracts']] = relationship('CustomerContracts', foreign_keys='[CustomerContracts.CustomerId]', back_populates='Accounts_')
    CustomerContracts_: Mapped[list['CustomerContracts']] = relationship('CustomerContracts', foreign_keys='[CustomerContracts.ReviewerId]', back_populates='Accounts1')
    DraftApprovals: Mapped[list['DraftApprovals']] = relationship('DraftApprovals', foreign_keys='[DraftApprovals.RequestedBy]', back_populates='Accounts_')
    DraftApprovals_: Mapped[list['DraftApprovals']] = relationship('DraftApprovals', foreign_keys='[DraftApprovals.ReviewerId]', back_populates='Accounts1')
    ContractReports: Mapped[list['ContractReports']] = relationship('ContractReports', foreign_keys='[ContractReports.AccusedId]', back_populates='Accounts_')
    ContractReports_: Mapped[list['ContractReports']] = relationship('ContractReports', foreign_keys='[ContractReports.ReporterId]', back_populates='Accounts1')
    ContractReports1: Mapped[list['ContractReports']] = relationship('ContractReports', foreign_keys='[ContractReports.ReviewedBy]', back_populates='Accounts2')


class ActivityTypes(Base):
    __tablename__ = 'ActivityTypes'
    __table_args__ = (
        ForeignKeyConstraint(['EventActivityId'], ['EventActivities.Id'], ondelete='RESTRICT', name='FK_ActivityTypes_EventActivities_EventActivityId'),
        PrimaryKeyConstraint('Id', name='PK_ActivityTypes'),
        Index('IX_ActivityTypes_EventActivityId', 'EventActivityId')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    EventActivityId: Mapped[int] = mapped_column(Integer, nullable=False)
    Name: Mapped[Optional[str]] = mapped_column(Text)
    IsDeleted: Mapped[Optional[bool]] = mapped_column(Boolean)

    EventActivities_: Mapped['EventActivities'] = relationship('EventActivities', back_populates='ActivityTypes')
    ActivityTypeGroups: Mapped[list['ActivityTypeGroups']] = relationship('ActivityTypeGroups', back_populates='ActivityTypes_')
    Rentals: Mapped[list['Rentals']] = relationship('Rentals', back_populates='ActivityTypes_')
    RobotTypeOfEvents: Mapped[list['RobotTypeOfEvents']] = relationship('RobotTypeOfEvents', back_populates='ActivityTypes_')


class AspNetRoleClaims(Base):
    __tablename__ = 'AspNetRoleClaims'
    __table_args__ = (
        ForeignKeyConstraint(['RoleId'], ['AspNetRoles.Id'], ondelete='CASCADE', name='FK_AspNetRoleClaims_AspNetRoles_RoleId'),
        PrimaryKeyConstraint('Id', name='PK_AspNetRoleClaims'),
        Index('IX_AspNetRoleClaims_RoleId', 'RoleId')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    RoleId: Mapped[str] = mapped_column(Text, nullable=False)
    ClaimType: Mapped[Optional[str]] = mapped_column(Text)
    ClaimValue: Mapped[Optional[str]] = mapped_column(Text)

    AspNetRoles_: Mapped['AspNetRoles'] = relationship('AspNetRoles', back_populates='AspNetRoleClaims')


class AspNetUserClaims(Base):
    __tablename__ = 'AspNetUserClaims'
    __table_args__ = (
        ForeignKeyConstraint(['UserId'], ['AspNetUsers.Id'], ondelete='CASCADE', name='FK_AspNetUserClaims_AspNetUsers_UserId'),
        PrimaryKeyConstraint('Id', name='PK_AspNetUserClaims'),
        Index('IX_AspNetUserClaims_UserId', 'UserId')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    UserId: Mapped[str] = mapped_column(Text, nullable=False)
    ClaimType: Mapped[Optional[str]] = mapped_column(Text)
    ClaimValue: Mapped[Optional[str]] = mapped_column(Text)

    AspNetUsers_: Mapped['AspNetUsers'] = relationship('AspNetUsers', back_populates='AspNetUserClaims')


class AspNetUserLogins(Base):
    __tablename__ = 'AspNetUserLogins'
    __table_args__ = (
        ForeignKeyConstraint(['UserId'], ['AspNetUsers.Id'], ondelete='CASCADE', name='FK_AspNetUserLogins_AspNetUsers_UserId'),
        PrimaryKeyConstraint('LoginProvider', 'ProviderKey', name='PK_AspNetUserLogins'),
        Index('IX_AspNetUserLogins_UserId', 'UserId')
    )

    LoginProvider: Mapped[str] = mapped_column(Text, primary_key=True)
    ProviderKey: Mapped[str] = mapped_column(Text, primary_key=True)
    UserId: Mapped[str] = mapped_column(Text, nullable=False)
    ProviderDisplayName: Mapped[Optional[str]] = mapped_column(Text)

    AspNetUsers_: Mapped['AspNetUsers'] = relationship('AspNetUsers', back_populates='AspNetUserLogins')


t_AspNetUserRoles = Table(
    'AspNetUserRoles', Base.metadata,
    Column('UserId', Text, primary_key=True),
    Column('RoleId', Text, primary_key=True),
    ForeignKeyConstraint(['RoleId'], ['AspNetRoles.Id'], ondelete='CASCADE', name='FK_AspNetUserRoles_AspNetRoles_RoleId'),
    ForeignKeyConstraint(['UserId'], ['AspNetUsers.Id'], ondelete='CASCADE', name='FK_AspNetUserRoles_AspNetUsers_UserId'),
    PrimaryKeyConstraint('UserId', 'RoleId', name='PK_AspNetUserRoles'),
    Index('IX_AspNetUserRoles_RoleId', 'RoleId')
)


class AspNetUserTokens(Base):
    __tablename__ = 'AspNetUserTokens'
    __table_args__ = (
        ForeignKeyConstraint(['UserId'], ['AspNetUsers.Id'], ondelete='CASCADE', name='FK_AspNetUserTokens_AspNetUsers_UserId'),
        PrimaryKeyConstraint('UserId', 'LoginProvider', 'Name', name='PK_AspNetUserTokens')
    )

    UserId: Mapped[str] = mapped_column(Text, primary_key=True)
    LoginProvider: Mapped[str] = mapped_column(Text, primary_key=True)
    Name: Mapped[str] = mapped_column(Text, primary_key=True)
    Value: Mapped[Optional[str]] = mapped_column(Text)

    AspNetUsers_: Mapped['AspNetUsers'] = relationship('AspNetUsers', back_populates='AspNetUserTokens')


class RobotAbilities(Base):
    __tablename__ = 'RobotAbilities'
    __table_args__ = (
        ForeignKeyConstraint(['RoboTypeId'], ['RoboTypes.Id'], name='FK_RobotAbilities_RoboTypes_RoboTypeId'),
        PrimaryKeyConstraint('Id', name='PK_RobotAbilities'),
        Index('IX_RobotAbilities_RoboTypeId', 'RoboTypeId')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    IsCustomizable: Mapped[bool] = mapped_column(Boolean, nullable=False)
    IsDeleted: Mapped[bool] = mapped_column(Boolean, nullable=False)
    RoboTypeId: Mapped[Optional[int]] = mapped_column(Integer)
    Ability: Mapped[Optional[str]] = mapped_column(Text)

    RoboTypes_: Mapped[Optional['RoboTypes']] = relationship('RoboTypes', back_populates='RobotAbilities')
    RentalDetails: Mapped[list['RentalDetails']] = relationship('RentalDetails', back_populates='RobotAbilities_')


class Robots(Base):
    __tablename__ = 'Robots'
    __table_args__ = (
        ForeignKeyConstraint(['RoboTypeId'], ['RoboTypes.Id'], name='FK_Robots_RoboTypes_RoboTypeId'),
        PrimaryKeyConstraint('Id', name='PK_Robots'),
        Index('IX_Robots_RoboTypeId', 'RoboTypeId')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    RoboTypeId: Mapped[Optional[int]] = mapped_column(Integer)
    RobotName: Mapped[Optional[str]] = mapped_column(Text)
    ModelName: Mapped[Optional[str]] = mapped_column(Text)
    Location: Mapped[Optional[str]] = mapped_column(Text)
    Specification: Mapped[Optional[str]] = mapped_column(Text)
    RobotStatus: Mapped[Optional[str]] = mapped_column(Text)
    IsDeleted: Mapped[Optional[bool]] = mapped_column(Boolean)
    Status: Mapped[Optional[str]] = mapped_column(Text)

    RoboTypes_: Mapped[Optional['RoboTypes']] = relationship('RoboTypes', back_populates='Robots')
    TypesOfRobos: Mapped[list['TypesOfRobos']] = relationship('TypesOfRobos', back_populates='Robots_')
    RobotInGroups: Mapped[list['RobotInGroups']] = relationship('RobotInGroups', back_populates='Robots_')


class ActivityTypeGroups(Base):
    __tablename__ = 'ActivityTypeGroups'
    __table_args__ = (
        ForeignKeyConstraint(['ActivityTypeId'], ['ActivityTypes.Id'], ondelete='CASCADE', name='FK_ActivityTypeGroups_ActivityTypes_ActivityTypeId'),
        PrimaryKeyConstraint('Id', name='PK_ActivityTypeGroups'),
        Index('IX_ActivityTypeGroups_ActivityTypeId', 'ActivityTypeId')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    ActivityTypeId: Mapped[int] = mapped_column(Integer, nullable=False)
    IsDeleted: Mapped[Optional[bool]] = mapped_column(Boolean)

    ActivityTypes_: Mapped['ActivityTypes'] = relationship('ActivityTypes', back_populates='ActivityTypeGroups')
    GroupSchedules: Mapped[list['GroupSchedules']] = relationship('GroupSchedules', back_populates='ActivityTypeGroups_')
    RobotInGroups: Mapped[list['RobotInGroups']] = relationship('RobotInGroups', back_populates='ActivityTypeGroups_')


class ContractTemplates(Base):
    __tablename__ = 'ContractTemplates'
    __table_args__ = (
        ForeignKeyConstraint(['CreatedBy'], ['Accounts.Id'], name='FK_ContractTemplates_Accounts_CreatedBy'),
        ForeignKeyConstraint(['UpdatedBy'], ['Accounts.Id'], name='FK_ContractTemplates_Accounts_UpdatedBy'),
        PrimaryKeyConstraint('Id', name='PK_ContractTemplates'),
        Index('IX_ContractTemplates_CreatedBy', 'CreatedBy'),
        Index('IX_ContractTemplates_UpdatedBy', 'UpdatedBy')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    CreatedAt: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    UpdatedAt: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    TemplateCode: Mapped[Optional[str]] = mapped_column(Text)
    Title: Mapped[Optional[str]] = mapped_column(Text)
    Description: Mapped[Optional[str]] = mapped_column(Text)
    BodyJson: Mapped[Optional[str]] = mapped_column(Text)
    Status: Mapped[Optional[str]] = mapped_column(Text)
    Version: Mapped[Optional[str]] = mapped_column(Text)
    CreatedBy: Mapped[Optional[int]] = mapped_column(Integer)
    UpdatedBy: Mapped[Optional[int]] = mapped_column(Integer)

    Accounts_: Mapped[Optional['Accounts']] = relationship('Accounts', foreign_keys=[CreatedBy], back_populates='ContractTemplates')
    Accounts1: Mapped[Optional['Accounts']] = relationship('Accounts', foreign_keys=[UpdatedBy], back_populates='ContractTemplates_')
    ContractDrafts: Mapped[list['ContractDrafts']] = relationship('ContractDrafts', back_populates='ContractTemplates_')
    TemplateClauses: Mapped[list['TemplateClauses']] = relationship('TemplateClauses', back_populates='ContractTemplates_')


class FaceProfiles(Base):
    __tablename__ = 'FaceProfiles'
    __table_args__ = (
        ForeignKeyConstraint(['AccountId'], ['Accounts.Id'], name='FK_FaceProfiles_Accounts_AccountId'),
        PrimaryKeyConstraint('Id', name='PK_FaceProfiles'),
        Index('IX_FaceProfiles_AccountId', 'AccountId')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    CitizenId: Mapped[str] = mapped_column(String(20), nullable=False)
    Embedding: Mapped[str] = mapped_column(Text, nullable=False)
    Model: Mapped[str] = mapped_column(String(50), nullable=False)
    HashSha256: Mapped[str] = mapped_column(String(64), nullable=False)
    CreatedAt: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    IsActive: Mapped[bool] = mapped_column(Boolean, nullable=False)
    AccountId: Mapped[Optional[int]] = mapped_column(Integer)
    FrontIdImagePath: Mapped[Optional[str]] = mapped_column(String(500))
    LastUsedAt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    Accounts_: Mapped[Optional['Accounts']] = relationship('Accounts', back_populates='FaceProfiles')
    FaceVerifications: Mapped[list['FaceVerifications']] = relationship('FaceVerifications', back_populates='FaceProfiles_')


class PaymentTransactions(Base):
    __tablename__ = 'PaymentTransactions'
    __table_args__ = (
        ForeignKeyConstraint(['AccountId'], ['Accounts.Id'], ondelete='CASCADE', name='FK_PaymentTransactions_Accounts_AccountId'),
        PrimaryKeyConstraint('Id', name='PK_PaymentTransactions'),
        Index('IX_PaymentTransactions_AccountId', 'AccountId')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    OrderCode: Mapped[int] = mapped_column(BigInteger, nullable=False)
    Amount: Mapped[int] = mapped_column(Integer, nullable=False)
    Description: Mapped[str] = mapped_column(Text, nullable=False)
    Status: Mapped[str] = mapped_column(Text, nullable=False)
    AccountId: Mapped[int] = mapped_column(Integer, nullable=False)
    CreatedAt: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    PaymentLinkId: Mapped[Optional[str]] = mapped_column(Text)
    UpdatedAt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    Accounts_: Mapped['Accounts'] = relationship('Accounts', back_populates='PaymentTransactions')
    ContractReports: Mapped[list['ContractReports']] = relationship('ContractReports', back_populates='PaymentTransactions_')


class Rentals(Base):
    __tablename__ = 'Rentals'
    __table_args__ = (
        ForeignKeyConstraint(['AccountId'], ['Accounts.Id'], ondelete='CASCADE', name='FK_Rentals_Accounts_AccountId'),
        ForeignKeyConstraint(['ActivityTypeId'], ['ActivityTypes.Id'], name='FK_Rentals_ActivityTypes_ActivityTypeId'),
        ForeignKeyConstraint(['EventActivityId'], ['EventActivities.Id'], name='FK_Rentals_EventActivities_EventActivityId'),
        ForeignKeyConstraint(['StaffId'], ['Accounts.Id'], name='FK_Rentals_Accounts_StaffId'),
        PrimaryKeyConstraint('Id', name='PK_Rentals'),
        Index('IX_Rentals_AccountId', 'AccountId'),
        Index('IX_Rentals_ActivityTypeId', 'ActivityTypeId'),
        Index('IX_Rentals_EventActivityId', 'EventActivityId'),
        Index('IX_Rentals_StaffId', 'StaffId')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    AccountId: Mapped[int] = mapped_column(Integer, nullable=False)
    EventName: Mapped[Optional[str]] = mapped_column(Text)
    PhoneNumber: Mapped[Optional[str]] = mapped_column(Text)
    Email: Mapped[Optional[str]] = mapped_column(Text)
    Description: Mapped[Optional[str]] = mapped_column(Text)
    Address: Mapped[Optional[str]] = mapped_column(Text)
    City: Mapped[Optional[str]] = mapped_column(Text)
    StartTime: Mapped[Optional[datetime.time]] = mapped_column(Time)
    EndTime: Mapped[Optional[datetime.time]] = mapped_column(Time)
    CreatedDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    UpdatedDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    RequestedDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    ReceivedDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    EventDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    IsDeleted: Mapped[Optional[bool]] = mapped_column(Boolean)
    Status: Mapped[Optional[str]] = mapped_column(Text)
    EventActivityId: Mapped[Optional[int]] = mapped_column(Integer)
    ActivityTypeId: Mapped[Optional[int]] = mapped_column(Integer)
    StaffId: Mapped[Optional[int]] = mapped_column(Integer)
    PlannedDeliveryTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    PlannedPickupTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    Accounts_: Mapped['Accounts'] = relationship('Accounts', foreign_keys=[AccountId], back_populates='Rentals')
    ActivityTypes_: Mapped[Optional['ActivityTypes']] = relationship('ActivityTypes', back_populates='Rentals')
    EventActivities_: Mapped[Optional['EventActivities']] = relationship('EventActivities', back_populates='Rentals')
    Accounts1: Mapped[Optional['Accounts']] = relationship('Accounts', foreign_keys=[StaffId], back_populates='Rentals_')
    ActualDeliveries: Mapped[list['ActualDeliveries']] = relationship('ActualDeliveries', back_populates='Rentals_')
    ChatRooms: Mapped[list['ChatRooms']] = relationship('ChatRooms', back_populates='Rentals_')
    ContractDrafts: Mapped[list['ContractDrafts']] = relationship('ContractDrafts', back_populates='Rentals_')
    FaceVerifications: Mapped[list['FaceVerifications']] = relationship('FaceVerifications', back_populates='Rentals_')
    GroupSchedules: Mapped[list['GroupSchedules']] = relationship('GroupSchedules', back_populates='Rentals_')
    PriceQuotes: Mapped[list['PriceQuotes']] = relationship('PriceQuotes', back_populates='Rentals_')
    RentalContracts: Mapped[list['RentalContracts']] = relationship('RentalContracts', back_populates='Rentals_')
    RentalDetails: Mapped[list['RentalDetails']] = relationship('RentalDetails', back_populates='Rentals_')


class RobotTypeOfEvents(Base):
    __tablename__ = 'RobotTypeOfEvents'
    __table_args__ = (
        ForeignKeyConstraint(['ActivityTypeId'], ['ActivityTypes.Id'], ondelete='CASCADE', name='FK_RobotTypeOfEvents_ActivityTypes_ActivityTypeId'),
        ForeignKeyConstraint(['RoboTypeId'], ['RoboTypes.Id'], ondelete='CASCADE', name='FK_RobotTypeOfEvents_RoboTypes_RoboTypeId'),
        PrimaryKeyConstraint('ActivityTypeId', 'RoboTypeId', name='PK_RobotTypeOfEvents'),
        Index('IX_RobotTypeOfEvents_RoboTypeId', 'RoboTypeId')
    )

    ActivityTypeId: Mapped[int] = mapped_column(Integer, primary_key=True)
    RoboTypeId: Mapped[int] = mapped_column(Integer, primary_key=True)
    Amount: Mapped[Optional[int]] = mapped_column(Integer)

    ActivityTypes_: Mapped['ActivityTypes'] = relationship('ActivityTypes', back_populates='RobotTypeOfEvents')
    RoboTypes_: Mapped['RoboTypes'] = relationship('RoboTypes', back_populates='RobotTypeOfEvents')


class TypesOfRobos(Base):
    __tablename__ = 'TypesOfRobos'
    __table_args__ = (
        ForeignKeyConstraint(['RoboTypeId'], ['RoboTypes.Id'], ondelete='CASCADE', name='FK_TypesOfRobos_RoboTypes_RoboTypeId'),
        ForeignKeyConstraint(['RobotId'], ['Robots.Id'], ondelete='CASCADE', name='FK_TypesOfRobos_Robots_RobotId'),
        PrimaryKeyConstraint('RobotId', 'RoboTypeId', name='PK_TypesOfRobos'),
        Index('IX_TypesOfRobos_RoboTypeId', 'RoboTypeId')
    )

    RobotId: Mapped[int] = mapped_column(Integer, primary_key=True)
    RoboTypeId: Mapped[int] = mapped_column(Integer, primary_key=True)
    IsDeleted: Mapped[Optional[bool]] = mapped_column(Boolean)

    RoboTypes_: Mapped['RoboTypes'] = relationship('RoboTypes', back_populates='TypesOfRobos')
    Robots_: Mapped['Robots'] = relationship('Robots', back_populates='TypesOfRobos')


class ActualDeliveries(Base):
    __tablename__ = 'ActualDeliveries'
    __table_args__ = (
        ForeignKeyConstraint(['RentalId'], ['Rentals.Id'], ondelete='CASCADE', name='FK_ActualDeliveries_Rentals_RentalId'),
        ForeignKeyConstraint(['StaffId'], ['Accounts.Id'], name='FK_ActualDeliveries_Accounts_StaffId'),
        PrimaryKeyConstraint('Id', name='PK_ActualDeliveries'),
        Index('IX_ActualDeliveries_RentalId', 'RentalId'),
        Index('IX_ActualDeliveries_StaffId', 'StaffId')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    RentalId: Mapped[int] = mapped_column(Integer, nullable=False)
    Status: Mapped[str] = mapped_column(Text, nullable=False)
    CreatedAt: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    StaffId: Mapped[Optional[int]] = mapped_column(Integer)
    ScheduledDeliveryTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    ActualDeliveryTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    ScheduledPickupTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    ActualPickupTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    CustomerRequestNotes: Mapped[Optional[str]] = mapped_column(Text)
    Notes: Mapped[Optional[str]] = mapped_column(Text)
    UpdatedAt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    Rentals_: Mapped['Rentals'] = relationship('Rentals', back_populates='ActualDeliveries')
    Accounts_: Mapped[Optional['Accounts']] = relationship('Accounts', back_populates='ActualDeliveries')


class ChatRooms(Base):
    __tablename__ = 'ChatRooms'
    __table_args__ = (
        ForeignKeyConstraint(['CustomerId'], ['Accounts.Id'], ondelete='CASCADE', name='FK_ChatRooms_Accounts_CustomerId'),
        ForeignKeyConstraint(['RentalId'], ['Rentals.Id'], ondelete='CASCADE', name='FK_ChatRooms_Rentals_RentalId'),
        ForeignKeyConstraint(['StaffId'], ['Accounts.Id'], ondelete='CASCADE', name='FK_ChatRooms_Accounts_StaffId'),
        PrimaryKeyConstraint('Id', name='PK_ChatRooms'),
        Index('IX_ChatRooms_CustomerId', 'CustomerId'),
        Index('IX_ChatRooms_RentalId', 'RentalId'),
        Index('IX_ChatRooms_StaffId', 'StaffId')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    RentalId: Mapped[int] = mapped_column(Integer, nullable=False)
    StaffId: Mapped[int] = mapped_column(Integer, nullable=False)
    CustomerId: Mapped[int] = mapped_column(Integer, nullable=False)
    CreatedAt: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    UpdatedAt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    Accounts_: Mapped['Accounts'] = relationship('Accounts', foreign_keys=[CustomerId], back_populates='ChatRooms')
    Rentals_: Mapped['Rentals'] = relationship('Rentals', back_populates='ChatRooms')
    Accounts1: Mapped['Accounts'] = relationship('Accounts', foreign_keys=[StaffId], back_populates='ChatRooms_')
    ChatMessages: Mapped[list['ChatMessages']] = relationship('ChatMessages', back_populates='ChatRooms_')


class ContractDrafts(Base):
    __tablename__ = 'ContractDrafts'
    __table_args__ = (
        ForeignKeyConstraint(['ContractTemplatesId'], ['ContractTemplates.Id'], name='FK_ContractDrafts_ContractTemplates_ContractTemplatesId'),
        ForeignKeyConstraint(['ManagerId'], ['Accounts.Id'], name='FK_ContractDrafts_Accounts_ManagerId'),
        ForeignKeyConstraint(['RentalId'], ['Rentals.Id'], name='FK_ContractDrafts_Rentals_RentalId'),
        ForeignKeyConstraint(['StaffId'], ['Accounts.Id'], name='FK_ContractDrafts_Accounts_StaffId'),
        PrimaryKeyConstraint('Id', name='PK_ContractDrafts'),
        Index('IX_ContractDrafts_ContractTemplatesId', 'ContractTemplatesId'),
        Index('IX_ContractDrafts_ManagerId', 'ManagerId'),
        Index('IX_ContractDrafts_RentalId', 'RentalId'),
        Index('IX_ContractDrafts_StaffId', 'StaffId')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    Title: Mapped[Optional[str]] = mapped_column(Text)
    BodyJson: Mapped[Optional[str]] = mapped_column(Text)
    Comments: Mapped[Optional[str]] = mapped_column(Text)
    Status: Mapped[Optional[str]] = mapped_column(Text)
    CreatedAt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    UpdatedAt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    ContractTemplatesId: Mapped[Optional[int]] = mapped_column(Integer)
    RentalId: Mapped[Optional[int]] = mapped_column(Integer)
    StaffId: Mapped[Optional[int]] = mapped_column(Integer)
    ManagerId: Mapped[Optional[int]] = mapped_column(Integer)

    ContractTemplates_: Mapped[Optional['ContractTemplates']] = relationship('ContractTemplates', back_populates='ContractDrafts')
    Accounts_: Mapped[Optional['Accounts']] = relationship('Accounts', foreign_keys=[ManagerId], back_populates='ContractDrafts')
    Rentals_: Mapped[Optional['Rentals']] = relationship('Rentals', back_populates='ContractDrafts')
    Accounts1: Mapped[Optional['Accounts']] = relationship('Accounts', foreign_keys=[StaffId], back_populates='ContractDrafts_')
    CustomerContracts: Mapped[list['CustomerContracts']] = relationship('CustomerContracts', back_populates='ContractDrafts_')
    DraftApprovals: Mapped[list['DraftApprovals']] = relationship('DraftApprovals', back_populates='ContractDrafts_')
    DraftClauses: Mapped[list['DraftClauses']] = relationship('DraftClauses', back_populates='ContractDrafts_')


class FaceVerifications(Base):
    __tablename__ = 'FaceVerifications'
    __table_args__ = (
        ForeignKeyConstraint(['AccountId'], ['Accounts.Id'], name='FK_FaceVerifications_Accounts_AccountId'),
        ForeignKeyConstraint(['FaceProfileId'], ['FaceProfiles.Id'], name='FK_FaceVerifications_FaceProfiles_FaceProfileId'),
        ForeignKeyConstraint(['RentalId'], ['Rentals.Id'], name='FK_FaceVerifications_Rentals_RentalId'),
        PrimaryKeyConstraint('Id', name='PK_FaceVerifications'),
        Index('IX_FaceVerifications_AccountId', 'AccountId'),
        Index('IX_FaceVerifications_FaceProfileId', 'FaceProfileId'),
        Index('IX_FaceVerifications_RentalId', 'RentalId')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    Threshold: Mapped[decimal.Decimal] = mapped_column(Numeric, nullable=False)
    Result: Mapped[str] = mapped_column(String(20), nullable=False)
    VerifiedAt: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    AccountId: Mapped[Optional[int]] = mapped_column(Integer)
    FaceProfileId: Mapped[Optional[int]] = mapped_column(Integer)
    MatchScore: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    RentalId: Mapped[Optional[int]] = mapped_column(Integer)
    ImageEvidenceRef: Mapped[Optional[str]] = mapped_column(String(200))

    Accounts_: Mapped[Optional['Accounts']] = relationship('Accounts', back_populates='FaceVerifications')
    FaceProfiles_: Mapped[Optional['FaceProfiles']] = relationship('FaceProfiles', back_populates='FaceVerifications')
    Rentals_: Mapped[Optional['Rentals']] = relationship('Rentals', back_populates='FaceVerifications')


class GroupSchedules(Base):
    __tablename__ = 'GroupSchedules'
    __table_args__ = (
        ForeignKeyConstraint(['ActivityTypeGroupId'], ['ActivityTypeGroups.Id'], name='FK_GroupSchedules_ActivityTypeGroups_ActivityTypeGroupId'),
        ForeignKeyConstraint(['RentalId'], ['Rentals.Id'], name='FK_GroupSchedules_Rentals_RentalId'),
        PrimaryKeyConstraint('Id', name='PK_GroupSchedules'),
        Index('IX_GroupSchedules_ActivityTypeGroupId', 'ActivityTypeGroupId'),
        Index('IX_GroupSchedules_RentalId', 'RentalId')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    IsDeleted: Mapped[bool] = mapped_column(Boolean, nullable=False)
    EventDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    EventLocation: Mapped[Optional[str]] = mapped_column(Text)
    EventCity: Mapped[Optional[str]] = mapped_column(Text)
    DeliveryTime: Mapped[Optional[datetime.time]] = mapped_column(Time)
    StartTime: Mapped[Optional[datetime.time]] = mapped_column(Time)
    EndTime: Mapped[Optional[datetime.time]] = mapped_column(Time)
    FinishTime: Mapped[Optional[datetime.time]] = mapped_column(Time)
    Status: Mapped[Optional[str]] = mapped_column(Text)
    ActivityTypeGroupId: Mapped[Optional[int]] = mapped_column(Integer)
    RentalId: Mapped[Optional[int]] = mapped_column(Integer)

    ActivityTypeGroups_: Mapped[Optional['ActivityTypeGroups']] = relationship('ActivityTypeGroups', back_populates='GroupSchedules')
    Rentals_: Mapped[Optional['Rentals']] = relationship('Rentals', back_populates='GroupSchedules')


class PriceQuotes(Base):
    __tablename__ = 'PriceQuotes'
    __table_args__ = (
        ForeignKeyConstraint(['ManagerId'], ['Accounts.Id'], name='FK_PriceQuotes_Accounts_ManagerId'),
        ForeignKeyConstraint(['RentalId'], ['Rentals.Id'], ondelete='CASCADE', name='FK_PriceQuotes_Rentals_RentalId'),
        PrimaryKeyConstraint('Id', name='PK_PriceQuotes'),
        Index('IX_PriceQuotes_ManagerId', 'ManagerId'),
        Index('IX_PriceQuotes_RentalId', 'RentalId')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    RentalId: Mapped[int] = mapped_column(Integer, nullable=False)
    Delivery: Mapped[Optional[float]] = mapped_column(Double(53))
    Deposit: Mapped[Optional[float]] = mapped_column(Double(53))
    Complete: Mapped[Optional[float]] = mapped_column(Double(53))
    Service: Mapped[Optional[float]] = mapped_column(Double(53))
    StaffDescription: Mapped[Optional[str]] = mapped_column(Text)
    ManagerFeedback: Mapped[Optional[str]] = mapped_column(Text)
    CustomerReason: Mapped[Optional[str]] = mapped_column(Text)
    CreatedAt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    IsDeleted: Mapped[Optional[bool]] = mapped_column(Boolean)
    Status: Mapped[Optional[str]] = mapped_column(Text)
    DeliveryFee: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    DeliveryDistance: Mapped[Optional[int]] = mapped_column(Integer)
    ManagerId: Mapped[Optional[int]] = mapped_column(Integer)
    SubmittedToManagerAt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    ManagerApprovedAt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    Accounts_: Mapped[Optional['Accounts']] = relationship('Accounts', back_populates='PriceQuotes')
    Rentals_: Mapped['Rentals'] = relationship('Rentals', back_populates='PriceQuotes')


class RentalContracts(Base):
    __tablename__ = 'RentalContracts'
    __table_args__ = (
        ForeignKeyConstraint(['RentalId'], ['Rentals.Id'], name='FK_RentalContracts_Rentals_RentalId'),
        PrimaryKeyConstraint('Id', name='PK_RentalContracts'),
        Index('IX_RentalContracts_RentalId', 'RentalId')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    Name: Mapped[Optional[str]] = mapped_column(Text)
    Description: Mapped[Optional[str]] = mapped_column(Text)
    IsDeleted: Mapped[Optional[bool]] = mapped_column(Boolean)
    Status: Mapped[Optional[str]] = mapped_column(Text)
    RentalId: Mapped[Optional[int]] = mapped_column(Integer)
    ContractUrl: Mapped[Optional[str]] = mapped_column(Text)

    Rentals_: Mapped[Optional['Rentals']] = relationship('Rentals', back_populates='RentalContracts')


class RentalDetails(Base):
    __tablename__ = 'RentalDetails'
    __table_args__ = (
        ForeignKeyConstraint(['RentalId'], ['Rentals.Id'], ondelete='CASCADE', name='FK_RentalDetails_Rentals_RentalId'),
        ForeignKeyConstraint(['RoboTypeId'], ['RoboTypes.Id'], ondelete='CASCADE', name='FK_RentalDetails_RoboTypes_RoboTypeId'),
        ForeignKeyConstraint(['RobotAbilityId'], ['RobotAbilities.Id'], name='FK_RentalDetails_RobotAbilities_RobotAbilityId'),
        PrimaryKeyConstraint('Id', name='PK_RentalDetails'),
        Index('IX_RentalDetails_RentalId', 'RentalId'),
        Index('IX_RentalDetails_RoboTypeId', 'RoboTypeId'),
        Index('IX_RentalDetails_RobotAbilityId', 'RobotAbilityId')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    RentalId: Mapped[int] = mapped_column(Integer, nullable=False)
    RoboTypeId: Mapped[int] = mapped_column(Integer, nullable=False)
    IsDeleted: Mapped[Optional[bool]] = mapped_column(Boolean)
    Status: Mapped[Optional[str]] = mapped_column(Text)
    RobotAbilityId: Mapped[Optional[int]] = mapped_column(Integer)
    Script: Mapped[Optional[str]] = mapped_column(Text)
    Branding: Mapped[Optional[str]] = mapped_column(Text)
    Scenario: Mapped[Optional[str]] = mapped_column(Text)

    Rentals_: Mapped['Rentals'] = relationship('Rentals', back_populates='RentalDetails')
    RoboTypes_: Mapped['RoboTypes'] = relationship('RoboTypes', back_populates='RentalDetails')
    RobotAbilities_: Mapped[Optional['RobotAbilities']] = relationship('RobotAbilities', back_populates='RentalDetails')


class RobotInGroups(Base):
    __tablename__ = 'RobotInGroups'
    __table_args__ = (
        ForeignKeyConstraint(['ActivityTypeGroupId'], ['ActivityTypeGroups.Id'], ondelete='CASCADE', name='FK_RobotInGroups_ActivityTypeGroups_ActivityTypeGroupId'),
        ForeignKeyConstraint(['RobotId'], ['Robots.Id'], ondelete='CASCADE', name='FK_RobotInGroups_Robots_RobotId'),
        PrimaryKeyConstraint('ActivityTypeGroupId', 'RobotId', name='PK_RobotInGroups'),
        Index('IX_RobotInGroups_RobotId', 'RobotId')
    )

    ActivityTypeGroupId: Mapped[int] = mapped_column(Integer, primary_key=True)
    RobotId: Mapped[int] = mapped_column(Integer, primary_key=True)
    IsDeleted: Mapped[Optional[bool]] = mapped_column(Boolean)

    ActivityTypeGroups_: Mapped['ActivityTypeGroups'] = relationship('ActivityTypeGroups', back_populates='RobotInGroups')
    Robots_: Mapped['Robots'] = relationship('Robots', back_populates='RobotInGroups')


class TemplateClauses(Base):
    __tablename__ = 'TemplateClauses'
    __table_args__ = (
        ForeignKeyConstraint(['ContractTemplatesId'], ['ContractTemplates.Id'], name='FK_TemplateClauses_ContractTemplates_ContractTemplatesId'),
        PrimaryKeyConstraint('Id', name='PK_TemplateClauses'),
        Index('IX_TemplateClauses_ContractTemplatesId', 'ContractTemplatesId')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    CreatedAt: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    ClauseCode: Mapped[Optional[str]] = mapped_column(Text)
    Title: Mapped[Optional[str]] = mapped_column(Text)
    Body: Mapped[Optional[str]] = mapped_column(Text)
    IsMandatory: Mapped[Optional[bool]] = mapped_column(Boolean)
    IsEditable: Mapped[Optional[bool]] = mapped_column(Boolean)
    ContractTemplatesId: Mapped[Optional[int]] = mapped_column(Integer)

    ContractTemplates_: Mapped[Optional['ContractTemplates']] = relationship('ContractTemplates', back_populates='TemplateClauses')
    DraftClauses: Mapped[list['DraftClauses']] = relationship('DraftClauses', back_populates='TemplateClauses_')


class ChatMessages(Base):
    __tablename__ = 'ChatMessages'
    __table_args__ = (
        ForeignKeyConstraint(['ChatRoomId'], ['ChatRooms.Id'], ondelete='CASCADE', name='FK_ChatMessages_ChatRooms_ChatRoomId'),
        ForeignKeyConstraint(['SenderId'], ['Accounts.Id'], ondelete='CASCADE', name='FK_ChatMessages_Accounts_SenderId'),
        PrimaryKeyConstraint('Id', name='PK_ChatMessages'),
        Index('IX_ChatMessages_ChatRoomId', 'ChatRoomId'),
        Index('IX_ChatMessages_SenderId', 'SenderId')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    ChatRoomId: Mapped[int] = mapped_column(Integer, nullable=False)
    SenderId: Mapped[int] = mapped_column(Integer, nullable=False)
    MessageType: Mapped[int] = mapped_column(Integer, nullable=False)
    Content: Mapped[str] = mapped_column(Text, nullable=False)
    IsRead: Mapped[bool] = mapped_column(Boolean, nullable=False)
    CreatedAt: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    MediaUrls: Mapped[Optional[str]] = mapped_column(Text)
    PriceQuoteId: Mapped[Optional[int]] = mapped_column(Integer)
    ContractId: Mapped[Optional[int]] = mapped_column(Integer)
    Status: Mapped[Optional[str]] = mapped_column(Text)

    ChatRooms_: Mapped['ChatRooms'] = relationship('ChatRooms', back_populates='ChatMessages')
    Accounts_: Mapped['Accounts'] = relationship('Accounts', back_populates='ChatMessages')


class CustomerContracts(Base):
    __tablename__ = 'CustomerContracts'
    __table_args__ = (
        ForeignKeyConstraint(['ContractDraftsId'], ['ContractDrafts.Id'], name='FK_CustomerContracts_ContractDrafts_ContractDraftsId'),
        ForeignKeyConstraint(['CustomerId'], ['Accounts.Id'], name='FK_CustomerContracts_Accounts_CustomerId'),
        ForeignKeyConstraint(['ReviewerId'], ['Accounts.Id'], name='FK_CustomerContracts_Accounts_ReviewerId'),
        PrimaryKeyConstraint('Id', name='PK_CustomerContracts'),
        Index('IX_CustomerContracts_ContractDraftsId', 'ContractDraftsId'),
        Index('IX_CustomerContracts_CustomerId', 'CustomerId'),
        Index('IX_CustomerContracts_ReviewerId', 'ReviewerId')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    ContractNumber: Mapped[Optional[str]] = mapped_column(Text)
    Status: Mapped[Optional[str]] = mapped_column(Text)
    SignedAt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    SentAt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    ContractUrl: Mapped[Optional[str]] = mapped_column(Text)
    CreatedAt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    ContractDraftsId: Mapped[Optional[int]] = mapped_column(Integer)
    CustomerId: Mapped[Optional[int]] = mapped_column(Integer)
    ReviewerId: Mapped[Optional[int]] = mapped_column(Integer)

    ContractDrafts_: Mapped[Optional['ContractDrafts']] = relationship('ContractDrafts', back_populates='CustomerContracts')
    Accounts_: Mapped[Optional['Accounts']] = relationship('Accounts', foreign_keys=[CustomerId], back_populates='CustomerContracts')
    Accounts1: Mapped[Optional['Accounts']] = relationship('Accounts', foreign_keys=[ReviewerId], back_populates='CustomerContracts_')


class DraftApprovals(Base):
    __tablename__ = 'DraftApprovals'
    __table_args__ = (
        ForeignKeyConstraint(['ContractDraftsId'], ['ContractDrafts.Id'], name='FK_DraftApprovals_ContractDrafts_ContractDraftsId'),
        ForeignKeyConstraint(['RequestedBy'], ['Accounts.Id'], name='FK_DraftApprovals_Accounts_RequestedBy'),
        ForeignKeyConstraint(['ReviewerId'], ['Accounts.Id'], name='FK_DraftApprovals_Accounts_ReviewerId'),
        PrimaryKeyConstraint('Id', name='PK_DraftApprovals'),
        Index('IX_DraftApprovals_ContractDraftsId', 'ContractDraftsId'),
        Index('IX_DraftApprovals_RequestedBy', 'RequestedBy'),
        Index('IX_DraftApprovals_ReviewerId', 'ReviewerId')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    Comments: Mapped[Optional[str]] = mapped_column(Text)
    Status: Mapped[Optional[str]] = mapped_column(Text)
    RequestedAt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    ReviewedAt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    ContractDraftsId: Mapped[Optional[int]] = mapped_column(Integer)
    RequestedBy: Mapped[Optional[int]] = mapped_column(Integer)
    ReviewerId: Mapped[Optional[int]] = mapped_column(Integer)

    ContractDrafts_: Mapped[Optional['ContractDrafts']] = relationship('ContractDrafts', back_populates='DraftApprovals')
    Accounts_: Mapped[Optional['Accounts']] = relationship('Accounts', foreign_keys=[RequestedBy], back_populates='DraftApprovals')
    Accounts1: Mapped[Optional['Accounts']] = relationship('Accounts', foreign_keys=[ReviewerId], back_populates='DraftApprovals_')


class DraftClauses(Base):
    __tablename__ = 'DraftClauses'
    __table_args__ = (
        ForeignKeyConstraint(['ContractDraftsId'], ['ContractDrafts.Id'], name='FK_DraftClauses_ContractDrafts_ContractDraftsId'),
        ForeignKeyConstraint(['TemplateClausesId'], ['TemplateClauses.Id'], name='FK_DraftClauses_TemplateClauses_TemplateClausesId'),
        PrimaryKeyConstraint('Id', name='PK_DraftClauses'),
        Index('IX_DraftClauses_ContractDraftsId', 'ContractDraftsId'),
        Index('IX_DraftClauses_TemplateClausesId', 'TemplateClausesId')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    Title: Mapped[Optional[str]] = mapped_column(Text)
    Body: Mapped[Optional[str]] = mapped_column(Text)
    IsModified: Mapped[Optional[bool]] = mapped_column(Boolean)
    CreatedAt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    ContractDraftsId: Mapped[Optional[int]] = mapped_column(Integer)
    TemplateClausesId: Mapped[Optional[int]] = mapped_column(Integer)

    ContractDrafts_: Mapped[Optional['ContractDrafts']] = relationship('ContractDrafts', back_populates='DraftClauses')
    TemplateClauses_: Mapped[Optional['TemplateClauses']] = relationship('TemplateClauses', back_populates='DraftClauses')
    ContractReports: Mapped[list['ContractReports']] = relationship('ContractReports', back_populates='DraftClauses_')


class ContractReports(Base):
    __tablename__ = 'ContractReports'
    __table_args__ = (
        ForeignKeyConstraint(['AccusedId'], ['Accounts.Id'], name='FK_ContractReports_Accounts_AccusedId'),
        ForeignKeyConstraint(['DraftClausesId'], ['DraftClauses.Id'], name='FK_ContractReports_DraftClauses_DraftClausesId'),
        ForeignKeyConstraint(['PaymentId'], ['PaymentTransactions.Id'], name='FK_ContractReports_PaymentTransactions_PaymentId'),
        ForeignKeyConstraint(['ReporterId'], ['Accounts.Id'], name='FK_ContractReports_Accounts_ReporterId'),
        ForeignKeyConstraint(['ReviewedBy'], ['Accounts.Id'], name='FK_ContractReports_Accounts_ReviewedBy'),
        PrimaryKeyConstraint('Id', name='PK_ContractReports'),
        Index('IX_ContractReports_AccusedId', 'AccusedId'),
        Index('IX_ContractReports_DraftClausesId', 'DraftClausesId'),
        Index('IX_ContractReports_PaymentId', 'PaymentId'),
        Index('IX_ContractReports_ReporterId', 'ReporterId'),
        Index('IX_ContractReports_ReviewedBy', 'ReviewedBy')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    DraftClausesId: Mapped[Optional[int]] = mapped_column(Integer)
    ReporterId: Mapped[Optional[int]] = mapped_column(Integer)
    ReportRole: Mapped[Optional[str]] = mapped_column(Text)
    AccusedId: Mapped[Optional[int]] = mapped_column(Integer)
    ReportCategory: Mapped[Optional[str]] = mapped_column(Text)
    Description: Mapped[Optional[str]] = mapped_column(Text)
    EvidencePath: Mapped[Optional[str]] = mapped_column(Text)
    Status: Mapped[Optional[str]] = mapped_column(Text)
    Resolution: Mapped[Optional[str]] = mapped_column(Text)
    CreatedAt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    ReviewedBy: Mapped[Optional[int]] = mapped_column(Integer)
    ReviewedAt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    ResolutionType: Mapped[Optional[str]] = mapped_column(Text)
    PaymentId: Mapped[Optional[int]] = mapped_column(Integer)

    Accounts_: Mapped[Optional['Accounts']] = relationship('Accounts', foreign_keys=[AccusedId], back_populates='ContractReports')
    DraftClauses_: Mapped[Optional['DraftClauses']] = relationship('DraftClauses', back_populates='ContractReports')
    PaymentTransactions_: Mapped[Optional['PaymentTransactions']] = relationship('PaymentTransactions', back_populates='ContractReports')
    Accounts1: Mapped[Optional['Accounts']] = relationship('Accounts', foreign_keys=[ReporterId], back_populates='ContractReports_')
    Accounts2: Mapped[Optional['Accounts']] = relationship('Accounts', foreign_keys=[ReviewedBy], back_populates='ContractReports1')
