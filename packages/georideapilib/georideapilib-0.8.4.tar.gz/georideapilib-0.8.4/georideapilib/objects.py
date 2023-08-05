"""
Georide objects implementation
@author Matthieu DUVAL <matthieu@duval-dev.fr>
"""
import time
import logging


_LOGGER = logging.getLogger(__name__)

class JsonMgtMetaClass(type):
    @staticmethod
    def json_field_protect(json, field_name, default_value = None):
        return json[field_name] if field_name in json.keys() else default_value
    
        

class GeoRideSharedTrip:
    """ Shared trip object representation """
    def __init__(self, url, shareId):
        self._url = url
        self._share_id = shareId

    @property
    def url(self):
        """ shared trip url """
        return self._url
    
    @property
    def share_id(self):
        """ shared trip id """
        return self._share_id

    @staticmethod
    def from_json(json):
        """return new object fromjson"""
        return GeoRideSharedTrip(
            json['url'],
            json['shareId']
        )

class GeoRideTrackerTrip:  # pylint: disable=too-many-instance-attributes
    """ Trip object representation """
    def __init__(self, trip_id, tracker_id, average_speed, max_speed, distance, duration, # pylint: disable=R0914, R0913
                 start_address, nice_start_address, start_lat, start_lon, end_address,
                 nice_end_address, end_lat, end_lon, start_time, end_time): 
        self._trip_id = trip_id
        self._tracker_id = tracker_id
        self._average_speed = average_speed
        self._max_speed = max_speed
        self._distance = distance
        self._duration = duration
        self._start_address = start_address
        self._nice_start_address = nice_start_address
        self._start_lat = start_lat
        self._start_lon = start_lon
        self._end_address = end_address
        self._nice_end_address = nice_end_address
        self._end_lat = end_lat
        self._end_lon = end_lon
        self._start_time = start_time
        self._end_time = end_time
    
    
    @property
    def trip_id(self):
        """trip_id  """
        return self._trip_id
    
    @property
    def tracker_id(self):
        """ tracker_id """
        return self._tracker_id
    
    @property
    def average_speed(self):
        """ average_speed """
        return self._average_speed
    
    @property
    def max_speed(self):
        """ max_speed """
        return self._max_speed
    
    @property
    def distance(self):
        """ distance """
        return self._distance
    
    @property
    def duration(self):
        """ duration """
        return self._duration
    
    @property
    def start_address(self):
        """ start_address """
        return self._start_address
    
    @property
    def nice_start_address(self):
        """ nice_start_address """
        return self._nice_start_address
    
    @property
    def start_lat(self):
        """ start_lat """
        return self._start_lat
    
    @property
    def start_lon(self):
        """ start_lon """
        return self._start_lon
    
    @property
    def end_address(self):
        """ end_address """
        return self._end_address
    
    @property
    def nice_end_address(self):
        """ nice_end_address """
        return self._nice_end_address
    
    @property
    def end_lat(self):
        """end_lat  """
        return self._end_lat
    
    @property
    def end_lon(self):
        """end_lon  """
        return self._end_lon
    
    @property
    def start_time(self):
        """ start_time """
        return self._start_time
    
    @property
    def end_time(self):
        """ end_time """
        return self._end_time

    
    @staticmethod
    def from_json(json):
        """return new object from json"""
        return GeoRideTrackerTrip(
            json['id'],
            json['trackerId'],
            json['averageSpeed'],
            json['maxSpeed'],
            json['distance'],
            json['duration'],
            json['startAddress'],
            json['niceStartAddress'],
            json['startLat'],
            json['startLon'],
            json['endAddress'],
            json['niceEndAddress'],
            json['endLat'],
            json['endLon'],
            json['startTime'],
            json['endTime']
        )

class GeoRideTrackerPosition:
    """ Tracker position object representation """
    def __init__(self, fixtime, latitude, longitude, altitude, speed, address): # pylint: disable= R0913
        self._fixtime = fixtime
        self._latitude = latitude
        self._longitude = longitude
        self._altitude = altitude
        self._speed = speed
        self._address = address

    @property
    def fixtime(self):
        """ fixtime """
        return self._fixtime

    @property
    def latitude(self):
        """ latitude """
        return self._latitude

    @property
    def longitude(self):
        """ longitude """
        return self._longitude

    @property
    def altitude(self):
        """ altitude """
        return self._altitude

    @property
    def speed(self):
        """ speed (m/s) """
        return self._speed

    @property
    def address(self):
        """ address """
        return self._address

    @staticmethod
    def from_json(json):
        """return new object fromjson"""
        return GeoRideTrackerPosition(
            json['fixtime'],
            json['latitude'],
            json['longitude'],
            json['altitude'],
            json['speed'],
            json['address']
        )

class GeoRideTracker(metaclass=JsonMgtMetaClass): # pylint: disable=R0904,R0902
    """ Tracker position object representation """
    def __init__(self, tracker_id, tracker_name, device_button_action, device_button_delay, # pylint: disable= R0913, R0914, R0915
                 vibration_level, is_old_tracker, auto_lock_freezed_to, fixtime, role,
                 last_payment_date, gift_card_id, expires, activation_date, odometer, is_stolen,
                 is_crashed, crash_detection_disabled, speed, moving, position_id, latitude, 
                 longitude, altitude, locked_position_id, locked_latitude, locked_longitude,
                 is_locked, can_see_position, can_lock, can_unlock, can_share, can_unshare,
                 can_check_speed, can_see_statistics, can_send_broken_down_signal,
                 can_send_stolen_signal, status, subscription_id, external_battery_voltage,
                 internal_battery_voltage, timezone, is_second_gen, is_up_to_date,
                 subscription, version, gift_card_expires, gift_card_months, odometer_updated_at,
                 maintenance_mode_until, battery_updated_at, is_in_eco, is_calibrated, 
                 is_oldsubscription, software_version, has_beacon, has_outdated_beacons, ecall_activated):
        self._tracker_id = tracker_id
        self._tracker_name = tracker_name
        self._device_button_action = device_button_action
        self._device_button_delay = device_button_delay
        self._vibration_level = vibration_level
        self._is_old_tracker = is_old_tracker
        self._position_id = position_id
        self._fixtime = fixtime
        self._latitude = latitude
        self._longitude = longitude
        self._altitude = altitude
        self._locked_position_id = locked_position_id
        self._locked_latitude = locked_latitude
        self._locked_longitude = locked_longitude
        self._role = role
        self._last_payment_date = last_payment_date
        self._gift_card_id = gift_card_id
        self._expires = expires
        self._activation_date = activation_date
        self._odometer = odometer
        self._is_locked = is_locked
        self._is_stolen = is_stolen
        self._is_crashed = is_crashed
        self._crash_detection_disabled = crash_detection_disabled
        self._speed = speed
        self._moving = moving
        self._can_see_position = can_see_position
        self._can_lock = can_lock
        self._can_unlock = can_unlock
        self._can_share = can_share
        self._can_unshare = can_unshare
        self._can_check_speed = can_check_speed
        self._can_see_statistics = can_see_statistics
        self._can_send_broken_down_signal = can_send_broken_down_signal
        self._can_send_stolen_signal = can_send_stolen_signal
        self._status = status
        self._auto_lock_freezed_to = auto_lock_freezed_to
        self._subscription_id = subscription_id
        self._external_battery_voltage = external_battery_voltage
        self._internal_battery_voltage = internal_battery_voltage
        self._timezone = timezone
        self._is_second_gen = is_second_gen
        self._is_up_to_date = is_up_to_date
        self._subscription = subscription
        self._version = version
        self._gift_card_expires = gift_card_expires
        self._gift_card_months = gift_card_months
        self._odometer_updated_at = odometer_updated_at
        self._maintenance_mode_until = maintenance_mode_until
        self._battery_updated_at = battery_updated_at
        self._is_in_eco = is_in_eco
        self._is_calibrated = is_calibrated
        self._is_oldsubscription = is_oldsubscription
        self._software_version = software_version
        self._has_beacon = has_beacon
        self._has_outdated_beacons = has_outdated_beacons
        self._ecall_activated = ecall_activated
        self._is_siren_on = False
        self._siren_last_on_date = time.time()

    @property
    def tracker_id(self):
        """ tracker_id """
        return self._tracker_id
    
    @property
    def tracker_name(self):
        """ tracker_name """
        return self._tracker_name
    
    @property
    def device_button_action(self):
        """ device_button_action """
        return self._device_button_action
    
    @property
    def device_button_delay(self):
        """ device_button_delay """
        return self._device_button_delay
    
    @property
    def vibration_level(self):
        """ vibration_level """
        return self._vibration_level
    
    @property
    def is_old_tracker(self):
        """ is_old_tracker """
        return self._is_old_tracker
    
    @property
    def auto_lock_freezed_to(self):
        """ auto_lock_freezed_to """
        return self._auto_lock_freezed_to
    
    @property
    def fixtime(self):
        """ fixtime """
        return self._fixtime
    
    @fixtime.setter
    def fixtime(self, fixtime):
        """ fixtime """
        self._fixtime = fixtime

    @property
    def role(self):
        """ role """
        return self._role
    
    @property
    def last_payment_date(self):
        """ last_payment_date """
        return self._last_payment_date
    
    @property
    def gift_card_id(self):
        """ gift_card_id """
        return self._gift_card_id
    
    @property
    def expires(self):
        """ expires """
        return self._expires
    
    @property
    def activation_date(self):
        """ activation_date """
        return self._activation_date
    
    @property
    def odometer(self):
        """ odometer """
        return self._odometer
    
    @property
    def is_stolen(self):
        """ is_stolen """
        return self._is_stolen

    @is_stolen.setter
    def is_stolen(self, is_stolen):
        """ is_stolen setter"""
        self._is_stolen = is_stolen
    
    @property
    def is_crashed(self):
        """ is_crashed """
        return self._is_crashed
    
    @is_crashed.setter
    def is_crashed(self, is_crashed):
        """ is_crashed setter"""
        self._is_crashed = is_crashed

    @property
    def crash_detection_disabled(self):
        """ crash_detection_disabled """
        return self._crash_detection_disabled
    
    @property
    def speed(self):
        """ speed """
        return self._speed
    
    @speed.setter
    def speed(self, speed):
        """ speed """
        self._speed = speed

    @property
    def moving(self):
        """ moving """
        return self._moving
    
    @moving.setter
    def moving(self, moving):
        """ moving """
        self._moving = moving

    @property
    def position_id(self):
        """ position_id """
        return self._position_id
    
    @property
    def latitude(self):
        """ latitude """
        return self._latitude
    
    @latitude.setter
    def latitude(self, latitude):
        """ latitude """
        self._latitude = latitude

    @property
    def longitude(self):
        """ longitude """
        return self._longitude
    
    @longitude.setter
    def longitude(self, longitude):
        """ longitude """
        self._longitude = longitude
    
    @property
    def altitude(self):
        """ altitude """
        return self._altitude
    
    @property
    def locked_position_id(self):
        """ locked_position_id """
        return self._locked_position_id
    
    @property
    def locked_latitude(self):
        """ locked_latitude """
        return self._locked_latitude
    
    @locked_latitude.setter
    def locked_latitude(self, locked_latitude):
        """ locked_latitude """
        self._locked_latitude = locked_latitude

    @property
    def locked_longitude(self):
        """ locked_longitude """
        return self._locked_longitude

    @locked_longitude.setter
    def locked_longitude(self, locked_longitude):
        """ locked_longitude """
        self._locked_longitude = locked_longitude

    @property
    def is_locked(self):
        """ is_locked """
        return self._is_locked
    
    @is_locked.setter
    def is_locked(self, is_locked):
        """ is_locked """
        self._is_locked = is_locked

    @property
    def can_see_position(self):
        """ can_see_position """
        return self._can_see_position
    
    @property
    def can_lock(self):
        """ can_lock """
        return self._can_lock
    
    @property
    def can_unlock(self):
        """ can_unlock """
        return self._can_unlock
    
    @property
    def can_share(self):
        """ can_share """
        return self._can_share
    
    @property
    def can_unshare(self):
        """ can_unshare """
        return self._can_unshare
    
    @property
    def can_check_speed(self):
        """ can_check_speed """
        return self._can_check_speed
    
    @property
    def can_see_statistics(self):
        """ can_see_statistics """
        return self._can_see_statistics
    
    @property
    def can_send_broken_down_signal(self):
        """ can_send_broken_down_signal """
        return self._can_send_broken_down_signal
    
    @property
    def can_send_stolen_signal(self):
        """ can_send_stolen_signal """
        return self._can_send_stolen_signal
    
    @property
    def status(self):
        """ status """
        return self._status

    @status.setter
    def status(self, status):
        """ status """
        self._status = status

    @property
    def subscription_id(self):
        """subscription_id property"""
        return self._subscription_id

    @property
    def external_battery_voltage(self):
        """_external_battery_voltage property"""
        return self._external_battery_voltage

    @property
    def internal_battery_voltage(self):
        """internal_battery_voltage property"""
        return self._internal_battery_voltage

    @property
    def timezone(self):
        """timezone property"""
        return self._timezone

    @property
    def is_second_gen(self):
        """is_second_gen property"""
        return self._is_second_gen

    @property
    def is_up_to_date(self):
        """is_up_to_date property"""
        return self._is_up_to_date

    @property
    def subscription(self):
        """ subscription property """
        return self._subscription

    @property
    def version(self):
        """ version property """
        return self._version

    @property
    def gift_card_expires(self):
        """ gift_card_expires property """
        return self._gift_card_expires

    @property
    def gift_card_months(self):
        """ gift_card_months property """
        return self._gift_card_months

    @property
    def odometer_updated_at(self):
        """ odometer_updated_at property """
        return self._odometer_updated_at

    @property
    def maintenance_mode_until(self):
        """ maintenance_mode_until property """
        return self._maintenance_mode_until

    @property
    def battery_updated_at(self):
        """ battery_updated_at property """
        return self._battery_updated_at

    @property
    def is_in_eco(self):
        """ is_in_eco property """
        return self._is_in_eco
    
    @is_in_eco.setter
    def is_in_eco(self, is_in_eco):
        """ is_in_eco setter """
        self._is_in_eco = is_in_eco

    @property
    def is_siren_on(self):
        """ is_siren_on property """
        return self._is_siren_on
    
    @is_siren_on.setter
    def is_siren_on(self, is_siren_on):
        """ is_siren_on setter """
        if is_siren_on:
            self._siren_last_on_date = time.time()
        self._is_siren_on = is_siren_on

    @property
    def siren_last_on_date(self):
        """ siren_last_on_date property """
        return self._siren_last_on_date

    @property
    def is_calibrated(self):
        """ is_calibrated property """
        return self._is_calibrated

    @property
    def is_oldsubscription(self):
        """ is_oldsubscription property """
        return self._is_oldsubscription
        
    @property
    def software_version(self):
        """ software_version property """
        return self._software_version

    @property
    def has_beacon(self):
        """ has_beacon property """
        return self._has_beacon

    @property
    def has_outdated_beacons(self):
        """ has_outdated_beacons property """
        return self._has_outdated_beacons

    @property
    def ecall_activated(self):
        """ ecall_activated property """
        return self._ecall_activated
        
    @classmethod
    def from_json(cls, json):
        """return new object fromjson"""
        return GeoRideTracker(
            json['trackerId'], # Mandatory
            json['trackerName'], # Mandatory
            cls.json_field_protect(json,'deviceButtonAction'),
            cls.json_field_protect(json,'deviceButtonDelay'),
            cls.json_field_protect(json,'vibrationLevel'),
            cls.json_field_protect(json,'isOldTracker', False),
            cls.json_field_protect(json,'autoLockFreezedTo'),
            cls.json_field_protect(json,'fixtime'),
            json['role'], # Mandatory
            json['lastPaymentDate'],# Mandatory
            cls.json_field_protect(json,'giftCardId'),
            cls.json_field_protect(json,'expires'),
            cls.json_field_protect(json,'activationDate'),
            json['odometer'],#Mandatory
            cls.json_field_protect(json,'isStolen', False),
            cls.json_field_protect(json,'isCrashed', False),
            cls.json_field_protect(json,'crashDetectionDisabled'),
            json['speed'], # Mandatory
            json['moving'], # Mandatory
            cls.json_field_protect(json,'positionId', -1),
            json['latitude'], # Mandatory
            json['longitude'], # Mandatory
            cls.json_field_protect(json,'altitude', 0),
            cls.json_field_protect(json,'lockedPositionId'),
            cls.json_field_protect(json,'lockedLatitude'),
            cls.json_field_protect(json,'lockedLongitude'),
            json['isLocked'], # Mandatory
            json['canSeePosition'],# Mandatory
            cls.json_field_protect(json,'canLock', False),
            cls.json_field_protect(json,'canUnlock', False),
            cls.json_field_protect(json,'canShare', False),
            cls.json_field_protect(json,'canUnshare', False),
            cls.json_field_protect(json,'canCheckSpeed', False),
            cls.json_field_protect(json,'canSeeStatistics', False),
            cls.json_field_protect(json,'canSendBrokenDownSignal', False),
            cls.json_field_protect(json,'canSendStolenSignal', False),
            json['status'],# Mandatory
            cls.json_field_protect(json,'subscriptionId'),
            cls.json_field_protect(json,'externalBatteryVoltage', -1.0),
            cls.json_field_protect(json,'internalBatteryVoltage', -1.0),
            cls.json_field_protect(json,'timezone', "Europe/Paris"),
            cls.json_field_protect(json,'isSecondGen', False),
            cls.json_field_protect(json,'isUpToDate', False),
            GeoRideSubscription.from_json(json['subscription']) if cls.json_field_protect(json,'subscription') is not None else None,
            cls.json_field_protect(json,'version', -1),
            cls.json_field_protect(json,'giftCardExpires'),
            cls.json_field_protect(json,'giftCardMonths'),
            cls.json_field_protect(json,'odometerUpdatedAt'),
            cls.json_field_protect(json,'maintenanceModeUntil'),
            cls.json_field_protect(json,'batteryUpdatedAt'),
            cls.json_field_protect(json,'isInEco', False),
            cls.json_field_protect(json,'isCalibrated', True),
            cls.json_field_protect(json,'isOldSubscription', True),
            cls.json_field_protect(json,'softwareVersion', -1),
            cls.json_field_protect(json,'hasBeacon', False),
            cls.json_field_protect(json,'hasOutdatedBeacons', False),
            cls.json_field_protect(json,'eCallActivated', False)
        )

    def update_all_data(self, tracker):
        """update all data of th tracker from anew object"""
        self._tracker_name = tracker.tracker_name
        self._device_button_action = tracker.device_button_action
        self._device_button_delay = tracker.device_button_delay
        self._vibration_level = tracker.vibration_level
        self._is_old_tracker = tracker.is_old_tracker
        self._position_id = tracker.position_id
        self._fixtime = tracker.fixtime
        self._latitude = tracker.latitude
        self._longitude = tracker.longitude
        self._altitude = tracker.altitude
        self._locked_position_id = tracker.locked_position_id
        self._locked_latitude = tracker.locked_latitude
        self._locked_longitude = tracker.locked_longitude
        self._role = tracker.role
        self._last_payment_date = tracker.last_payment_date
        self._gift_card_id = tracker.gift_card_id 
        self._expires = tracker.expires
        self._activation_date = tracker.activation_date
        self._odometer = tracker.odometer
        self._is_locked = tracker.is_locked
        self._is_stolen = tracker.is_stolen
        self._is_crashed = tracker.is_crashed
        self._crash_detection_disabled = tracker.crash_detection_disabled
        self._speed = tracker.speed
        self._moving = tracker.moving
        self._can_see_position = tracker.can_see_position
        self._can_lock = tracker.can_lock
        self._can_unlock = tracker.can_unlock
        self._can_share = tracker.can_share
        self._can_unshare = tracker.can_unshare
        self._can_check_speed = tracker.can_check_speed
        self._can_see_statistics = tracker.can_see_statistics
        self._can_send_broken_down_signal = tracker.can_send_broken_down_signal
        self._can_send_stolen_signal = tracker.can_send_stolen_signal
        self._status = tracker.status
        self._auto_lock_freezed_to = tracker.auto_lock_freezed_to
        self._subscription_id = tracker.subscription_id
        self._external_battery_voltage = tracker.external_battery_voltage
        self._internal_battery_voltage = tracker.internal_battery_voltage
        self._timezone = tracker.timezone
        self._is_second_gen = tracker.is_second_gen
        self._is_up_to_date = tracker.is_up_to_date
        self._subscription = tracker.subscription
        self._version = tracker.version
        self._gift_card_expires = tracker.gift_card_expires
        self._gift_card_months = tracker.gift_card_months
        self._odometer_updated_at = tracker.odometer_updated_at
        self._maintenance_mode_until = tracker.maintenance_mode_until
        self._battery_updated_at = tracker.battery_updated_at
        self._is_in_eco = tracker.is_in_eco
        self._is_calibrated = tracker.is_calibrated
        self._is_oldsubscription = tracker.is_oldsubscription
        self._software_version = tracker.software_version
        self._has_beacon = tracker.has_beacon
        self._has_outdated_beacons = tracker.has_outdated_beacons
        self._ecall_activated = tracker.ecall_activated

class GeoRideTrackerBeacon:
    """ GeoRideTrackerBeacon representation """ 
    def __init__(self, beacon_id, linked_tracker_id, name, created_at, updated_at,
                 mac_address, battery_level, last_battery_level_update, sleep_delay,
                 is_updated, power):
        self._beacon_id = beacon_id
        self._linked_tracker_id = linked_tracker_id
        self._name = name
        self._created_at = created_at
        self._updated_at = updated_at
        self._mac_address = mac_address
        self._battery_level = battery_level
        self._last_battery_level_update = last_battery_level_update
        self._sleep_delay = sleep_delay
        self._is_updated = is_updated
        self._power = power


    @property
    def linked_tracker_id(self):
        """ linked_tracker_id property """
        return self._linked_tracker_id
    
    @linked_tracker_id.setter
    def linked_tracker_id(self, linked_tracker_id):
        """ linked_tracker_id setter """
        self._linked_tracker_id = linked_tracker_id

    @property
    def beacon_id(self):
        """beacon_id property"""
        return self._beacon_id

    @property
    def name(self):
        """name property"""
        return self._name

    @property
    def created_at(self):
        """created_at property"""
        return self._created_at

    @property
    def updated_at(self):
        """updated_at property"""
        return self._updated_at

    @property
    def mac_address(self):
        """mac_address property"""
        return self._mac_address

    @property
    def battery_level(self):
        """battery_level property"""
        return self._battery_level

    @property
    def last_battery_level_update(self):
        """last_battery_level_update property"""
        return self._last_battery_level_update

    @property
    def sleep_delay(self):
        """sleep_delay property"""
        return self._sleep_delay

    @property
    def is_updated(self):
        """is_updated property"""
        return self._is_updated

    @property
    def power(self):
        """power property"""
        return self._power

    @classmethod
    def from_json(cls, json):
        """return new object from_json"""
        return GeoRideTrackerBeacon(
            json['id'],
            json['linked_tracker_id'],
            json['name'],
            json['createdAt'],
            json['updatedAt'],
            json['macAddress'],
            json['batteryLevel'],
            json['lastBatteryLevelUpdate'],
            json['sleepDelay'],
            json['isUpdated'],
            json['power'])
    
    def update_all_data(self, tracker_beacon):
        """update all data of the tracker beacon from a new object"""
        self._name = tracker_beacon.name
        self._created_at = tracker_beacon.created_at
        self._updated_at = tracker_beacon.updated_at
        self._mac_address = tracker_beacon.mac_address
        self._battery_level = tracker_beacon.battery_level
        self._last_battery_level_update = tracker_beacon.last_battery_level_update
        self._sleep_delay = tracker_beacon.sleep_delay
        self._is_updated = tracker_beacon.is_updated
        self._power = tracker_beacon.power


class GeoRideSubscription(metaclass=JsonMgtMetaClass):
    """ Account object representation """ 
    def __init__(self, subscription_id, subscription_type, initial_date, next_payment_date,
                status, paused_since, cancel_requested, price, first_name, last_name, card_information):
        self._subscription_id = subscription_id
        self._subscription_type = subscription_type
        self._initial_date = initial_date
        self._next_payment_date = next_payment_date
        self._status = status
        self._paused_since = paused_since
        self._cancel_requested = cancel_requested
        self._price = price
        self._first_name = first_name
        self._last_name = last_name
        self._card_information = card_information

    @property
    def subscription_id(self):
        """subscription_id property"""
        return self._subscription_id

    @property
    def subscription_type(self):
        """subscription_type property"""
        return self._subscription_type

    @property
    def initial_date(self):
        """initial_date property"""
        return self._initial_date

    @property
    def next_payment_date(self):
        """next_payment_date property"""
        return self._next_payment_date

    @property
    def status(self):
        """status property"""
        return self._status

    @property
    def paused_since(self):
        """paused_since property"""
        return self._paused_since

    @property
    def cancel_requested(self):
        """cancel_requested property"""
        return self._cancel_requested

    @property
    def price(self):
        """price property"""
        return self._price

    @property
    def first_name(self):
        """first_name property"""
        return self._first_name

    @property
    def last_name(self):
        """last_name property"""
        return self._last_name

    @property
    def card_information(self):
        """card_information property"""
        return self._card_information

    @classmethod
    def from_json(cls, json):
        """return new object from_json"""
        card_info = GeoRideSubscription_CardInfo.from_json(json['cardInformation']) if cls.json_field_protect(json, 'cardInformation', None) is not None else {}
        return GeoRideSubscription(
            json['id'],
            json['type'],
            cls.json_field_protect(json, 'initialDate'),
            cls.json_field_protect(json, 'nextPaymentDate'),
            cls.json_field_protect(json, 'status'),
            cls.json_field_protect(json, 'pausedSince'),
            cls.json_field_protect(json, 'cancelRequested'),
            cls.json_field_protect(json, 'price'),
            cls.json_field_protect(json, 'firstName'),
            cls.json_field_protect(json, 'lastName'),
            card_info
        )

class GeoRideSubscription_CardInfo(metaclass=JsonMgtMetaClass):
    """ Account object representation """ 
    def __init__(self, last_digits, expiry, brand):
        self._last_digits = last_digits
        self._expiry = expiry
        self._brand = brand
   
    @property
    def last_digits(self):
        """last_digits property"""
        return self._last_digits

    @property
    def expiry(self):
        """expiry property"""
        return self._expiry

    @property
    def brand(self):
        """brand property"""
        return self._brand


    @classmethod
    def from_json(cls, json):
        """return new object from_json"""
        return GeoRideSubscription_CardInfo(
            cls.json_field_protect(json, 'lastDigits'),
            cls.json_field_protect(json, 'expiry'),
            cls.json_field_protect(json, 'brand')
        )

class GeoRideAccount:
    """ Account object representation """ 
    def __init__(self, account_id, email, is_admin, auth_token):
        self._account_id = account_id
        self._email = email
        self._is_admin = is_admin
        self._auth_token = auth_token

    @property
    def account_id(self):
        """ account_id """
        return self._account_id

    @property
    def email(self):
        """ email """
        return self._email

    @property
    def is_admin(self):
        """ is_admin """
        return self._is_admin

    @property
    def auth_token(self):
        """ auth_token """
        return self._auth_token

    @auth_token.setter
    def auth_token(self, new_token):
        """ change auth_token """
        self._auth_token = new_token

    @staticmethod
    def from_json(json):
        """return new object from_json"""
        return GeoRideAccount(
            json['id'],
            json['email'],
            json['isAdmin'],
            json['authToken']
        )

class GeoRideUser: # pylint: disable= R0902
    """ User object representation """ 
    def __init__(self, user_id, email, first_name, created_at, phone_number, # pylint: disable= R0913
                 push_user_token, legal, date_of_birth): 
        self._user_id = user_id
        self._email = email
        self._first_name = first_name
        self._created_at = created_at
        self._phone_number = phone_number
        self._push_user_token = push_user_token
        self._legal = legal
        self._date_of_birth = date_of_birth

    @property
    def user_id(self):
        """ user_id """
        return self._user_id

    @property
    def email(self):
        """ email """
        return self._email

    @property
    def first_name(self):
        """ first_name """
        return self._first_name

    @property
    def created_at(self):
        """ created_at """
        return self._created_at
    
    @property
    def phone_number(self):
        """ phone_number """
        return self._phone_number
    
    @property
    def push_user_token(self):
        """ push_user_token """
        return self._push_user_token
    
    @property
    def legal(self):
        """ legal """
        return self._legal

    @property
    def date_of_birth(self):
        """ date_ofo_birth """
        return self._date_of_birth

    @staticmethod
    def from_json(json):
        """return new object fromjson"""
        return GeoRideUser(
            json['id'],
            json['email'],
            json['firstName'],
            json['createdAt'],
            json['phoneNumber'],
            json['pushUserToken'],
            json['legal'],
            json['dateOfBirth']
        )