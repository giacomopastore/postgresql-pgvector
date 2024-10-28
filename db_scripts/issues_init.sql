-- TODO: Create IVFFlat index

CREATE TABLE issues (
  id SERIAL PRIMARY KEY,
  issue_date DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  brand VARCHAR(255) NOT NULL,
  model VARCHAR(255) NOT NULL,
  issue TEXT NOT NULL CHECK (ISSUE != ''),
  fix TEXT NOT NULL CHECK (FIX != ''),
  issue_embedding vector(1024)
);

INSERT INTO issues (issue_date, brand, model, issue, fix) 
VALUES 
('2022-01-01', 'Samsung', 'Galaxy S22', 'Battery drains quickly even on standby.', 'Replaced the battery'),
('2021-12-05', 'Apple', 'iPhone 12', 'Touchscreen is unresponsive on the edges.', 'Replaced the screen'),
('2022-02-15', 'Google', 'Pixel 6', 'Phone reboots randomly during use.', 'Updated the firmware and checked for software issues'),
('2021-11-10', 'OnePlus', 'Nord 2', 'Wi-Fi disconnects frequently.', 'Reset network settings and updated the firmware'),
('2022-03-20', 'Huawei', 'P40 Pro', 'Camera produces blurry images.', 'Cleaned the lens and recalibrated the camera'),
('2021-12-10', 'Xiaomi', 'Redmi Note 10', 'Fingerprint scanner not recognizing any fingerprints.', 'Recalibrated the scanner and cleaned the sensor'),
('2022-01-20', 'LG', 'V60 ThinQ', 'Screen flickers at low brightness.', 'Adjusted the backlight and updated the firmware'),
('2021-11-15', 'Sony', 'Xperia 5 III', 'Phone heats up during video calls.', 'Cleaned vents and applied thermal paste'),
('2022-02-10', 'Oppo', 'Reno 5', 'Charging is very slow even with original charger.', 'Checked charging port and replaced battery'),
('2021-12-25', 'Asus', 'ROG Phone 5', 'Sound crackles during gaming.', 'Updated audio drivers and cleaned the speakers'),
('2022-01-05', 'Motorola', 'Edge 20', 'GPS signal is weak and inconsistent.', 'Updated GPS drivers and reset location settings'),
('2022-02-20', 'Samsung', 'Galaxy Note 20', 'Screen has a yellow tint.', 'Recalibrated display and adjusted color settings'),
('2021-11-30', 'Apple', 'iPhone SE', 'No audio during calls but works with loudspeaker.', 'Replaced earpiece and checked audio settings'),
('2022-01-25', 'Google', 'Pixel 4a', 'Battery drains after update.', 'Replaced battery and rolled back software update'),
('2021-12-05', 'OnePlus', '7T', 'Bluetooth connectivity issues.', 'Reset Bluetooth settings and updated firmware'),
('2022-03-05', 'Huawei', 'Nova 7i', 'Notifications are delayed.', 'Checked notification settings and updated firmware'),
('2021-12-15', 'Xiaomi', 'Mi 11 Lite', 'Camera app crashes after opening.', 'Reinstalled camera app and updated firmware'),
('2022-02-05', 'LG', 'G7 ThinQ', 'Proximity sensor not working.', 'Recalibrated sensor and cleaned the area'),
('2021-11-22', 'Sony', 'Xperia 10 II', 'Device freezes during calls.', 'Updated firmware and cleared cache'),
('2022-03-15', 'Oppo', 'Find X2', 'Keyboard input lagging.', 'Reset keyboard app and cleared cache'),
('2022-01-10', 'Asus', 'Zenfone 8', 'Phone restarts when connecting to Bluetooth.', 'Reinstalled Bluetooth drivers'),
('2021-11-30', 'Motorola', 'Moto G Power', 'Battery does not charge beyond 80%.', 'Replaced battery and recalibrated'),
('2022-02-15', 'Samsung', 'Galaxy S21', 'App crashes after update.', 'Cleared app cache and reinstalled updates'),
('2021-12-10', 'Apple', 'iPhone XR', 'Face ID is not recognizing.', 'Recalibrated Face ID and cleaned sensors'),
('2022-01-30', 'Google', 'Pixel 3', 'Phone vibrates constantly.', 'Rebooted and updated software'),
('2021-11-20', 'OnePlus', '8T', 'Screen does not rotate automatically.', 'Checked sensors and reset display settings'),
('2022-03-05', 'Huawei', 'Y9a', 'Front camera does not retract.', 'Reset camera module and updated firmware'),
('2021-12-25', 'Xiaomi', 'Redmi 9', 'Touch response is delayed.', 'Cleaned screen and reset touch sensitivity'),
('2022-01-15', 'LG', 'Wing', 'Phone reboots during calls.', 'Updated firmware and reset network settings'),
('2021-11-10', 'Sony', 'Xperia 1', 'Battery drains excessively on standby.', 'Replaced battery'),
('2022-02-28', 'Oppo', 'A74', 'USB connection is unstable.', 'Cleaned charging port and checked cable'),
('2021-12-15', 'Asus', 'ROG Phone 3', 'Game crashes frequently.', 'Updated game and cleared cache'),
('2022-01-05', 'Motorola', 'Moto G60', 'Screen flickers in low-light mode.', 'Adjusted display settings and updated firmware'),
('2021-11-18', 'Samsung', 'Galaxy Fold 2', 'Folding screen has crease lines.', 'Checked display, advised screen protector'),
('2022-02-15', 'Apple', 'iPhone 11', 'Battery percentage fluctuates.', 'Replaced battery and updated firmware'),
('2021-12-20', 'Google', 'Pixel 5a', 'Google Assistant not responding.', 'Reset assistant and cleared cache'),
('2022-01-12', 'OnePlus', 'Nord N10', 'Cannot connect to 5G network.', 'Updated network drivers and reset settings'),
('2021-11-25', 'Huawei', 'P30', 'Camera shutter sound cannot be muted.', 'Updated camera app and checked settings'),
('2022-03-02', 'Xiaomi', 'Mi 9T', 'Phone lags after update.', 'Rolled back update and cleared cache'),
('2021-12-12', 'LG', 'K92', 'Flashlight button not working.', 'Reset flashlight and updated settings'),
('2022-01-08', 'Sony', 'Xperia 10', 'Phone fails to wake up from sleep.', 'Rebooted and updated software'),
('2021-11-19', 'Oppo', 'A53', 'Screen has ghosting issues.', 'Recalibrated display and cleaned screen'),
('2022-02-12', 'Asus', 'Zenfone Max Pro', 'Cannot take screenshots.', 'Updated software and reset settings'),
('2021-12-10', 'Motorola', 'Edge+', 'Wi-Fi signal drops often.', 'Reset network settings and updated firmware'),
('2022-03-10', 'Samsung', 'Galaxy Z Flip', 'Screen protector peeling.', 'Replaced protector and checked display'),
('2021-11-27', 'Apple', 'iPhone 8', 'Cannot hear calls without speaker.', 'Replaced earpiece and tested audio settings'),
('2022-02-25', 'Google', 'Pixel 6 Pro', 'Phone does not vibrate for notifications.', 'Checked vibration settings and rebooted'),
('2021-12-18', 'OnePlus', '9 Pro', 'Screen randomly dims.', 'Adjusted brightness settings and updated firmware'),
('2022-01-15', 'Huawei', 'Nova 8', 'Cannot connect to mobile data.', 'Reset network settings and updated firmware'),
('2021-11-30', 'Xiaomi', 'Mi 8', 'Power button unresponsive.', 'Replaced button and checked connections'),
('2022-03-20', 'Samsung', 'Galaxy A52', 'Phone loses signal frequently.', 'Reset network settings and replaced SIM card'),
('2021-12-02', 'Apple', 'iPhone 11 Pro', 'Low volume during calls.', 'Replaced earpiece and cleaned speaker'),
('2022-02-14', 'Google', 'Pixel 5a', 'Battery percentage stuck at 100%.', 'Rebooted phone and recalibrated battery'),
('2021-11-12', 'OnePlus', '6T', 'Random screen flickering.', 'Updated firmware and adjusted display settings'),
('2022-03-01', 'Huawei', 'Mate 20 Pro', 'No sound from headphones.', 'Cleaned headphone jack and updated drivers'),
('2021-12-22', 'Xiaomi', 'Poco F3', 'Phone cannot detect Wi-Fi networks.', 'Reset Wi-Fi settings and updated firmware'),
('2022-01-25', 'LG', 'G6', 'Overheating when charging.', 'Replaced charger and cleaned charging port'),
('2021-11-05', 'Sony', 'Xperia L4', 'App icons missing from home screen.', 'Cleared cache and rebooted phone'),
('2022-02-18', 'Oppo', 'A95', 'Notifications are silent even with sound on.', 'Checked notification settings and reset preferences'),
('2021-12-14', 'Asus', 'Zenfone 7 Pro', 'Touchscreen not detecting multi-touch.', 'Replaced touchscreen and recalibrated'),
('2022-01-12', 'Motorola', 'Moto G30', 'Screen is unresponsive when charging.', 'Cleaned screen and recalibrated touch sensors'),
('2022-02-25', 'Samsung', 'Galaxy A32', 'Slow charging even with fast charger.', 'Replaced charging port and updated software'),
('2021-11-30', 'Apple', 'iPhone 7', 'Camera flash not working.', 'Replaced flash component and checked settings'),
('2022-01-28', 'Google', 'Pixel 3 XL', 'Screen has green tint.', 'Adjusted color calibration and updated firmware'),
('2021-12-06', 'OnePlus', '7 Pro', 'Face unlock not functioning.', 'Reset face unlock settings and recalibrated camera'),
('2022-03-06', 'Huawei', 'P Smart', 'Phone doesn’t vibrate for calls.', 'Checked vibration settings and replaced motor'),
('2021-12-10', 'Xiaomi', 'Mi A2', 'Brightness automatically dims.', 'Adjusted display settings and updated firmware'),
('2022-02-12', 'LG', 'V40 ThinQ', 'Screen keeps rotating randomly.', 'Calibrated gyroscope and reset display settings'),
('2021-11-08', 'Sony', 'Xperia Z5', 'Wi-Fi keeps dropping.', 'Reset network settings and checked for firmware issues'),
('2022-03-08', 'Oppo', 'F19', 'Screen unresponsive at times.', 'Rebooted and recalibrated touchscreen'),
('2022-01-11', 'Asus', 'Zenfone 6', 'Device restarts when opening camera.', 'Updated firmware and replaced camera app'),
('2021-11-21', 'Motorola', 'Moto Z', 'Speaker sounds muffled.', 'Cleaned speaker and updated drivers'),
('2022-02-05', 'Samsung', 'Galaxy Note 9', 'S-Pen is unresponsive.', 'Replaced S-Pen battery and recalibrated sensor'),
('2021-12-11', 'Apple', 'iPhone 6s', 'Touch ID not working.', 'Replaced fingerprint sensor and recalibrated'),
('2022-01-17', 'Google', 'Pixel 2', 'Bluetooth disconnects randomly.', 'Reset Bluetooth settings and updated firmware'),
('2021-11-26', 'OnePlus', 'Nord CE', 'No notifications on lock screen.', 'Checked notification settings and cleared cache'),
('2022-03-10', 'Huawei', 'Mate 10', 'Proximity sensor always active.', 'Recalibrated sensor and cleaned screen'),
('2021-12-03', 'Xiaomi', 'Mi Mix 3', 'Face unlock not recognizing in low light.', 'Recalibrated camera and adjusted settings'),
('2022-02-06', 'LG', 'Q60', 'Phone randomly disconnects from charger.', 'Replaced charging port and checked cable'),
('2021-11-27', 'Sony', 'Xperia 1 III', 'GPS is inaccurate.', 'Updated GPS drivers and reset location settings'),
('2022-01-19', 'Oppo', 'A93', 'Screen doesn’t turn off during calls.', 'Recalibrated proximity sensor and updated firmware'),
('2021-12-15', 'Asus', 'ROG Phone 2', 'Screen is black after reboot.', 'Updated software and rebooted phone'),
('2022-01-07', 'Motorola', 'One Vision', 'Fingerprint sensor stopped working.', 'Recalibrated sensor and cleaned area'),
('2022-02-13', 'Samsung', 'Galaxy S20 FE', 'Screen edges not responsive.', 'Replaced screen and recalibrated touch'),
('2021-11-13', 'Apple', 'iPhone X', 'Screen brightness fluctuates.', 'Replaced display and adjusted settings'),
('2022-03-18', 'Google', 'Pixel 4', 'Lags when unlocking.', 'Recalibrated face unlock and cleared cache'),
('2021-12-24', 'OnePlus', '5', 'Phone freezes when receiving calls.', 'Updated firmware and cleared app cache'),
('2022-01-02', 'Huawei', 'Honor 10', 'Volume button stuck.', 'Replaced button and cleaned internals'),
('2022-02-20', 'Xiaomi', 'Redmi 7', 'Charging indicator not showing.', 'Cleaned charging port and rebooted phone'),
('2021-11-22', 'LG', 'K51', 'Photos are saved upside down.', 'Calibrated gyroscope and adjusted camera settings'),
('2022-03-12', 'Sony', 'Xperia XZ2', 'Cannot send text messages.', 'Reset network settings and updated firmware'),
('2022-01-24', 'Oppo', 'Find X', 'Battery drains during standby.', 'Replaced battery and updated software'),
('2021-12-27', 'Asus', 'Zenfone 5', 'Screen flickers during videos.', 'Adjusted brightness settings and updated drivers'),
('2022-02-10', 'Motorola', 'G7 Plus', 'Camera focus is slow.', 'Recalibrated camera and updated firmware'),
('2021-11-17', 'Samsung', 'Galaxy S10', 'Phone gets warm on standby.', 'Checked for app issues and cleared cache'),
('2022-01-13', 'Apple', 'iPhone 8 Plus', 'Audio only plays on one side with headphones.', 'Replaced audio jack and tested settings'),
('2022-03-14', 'Google', 'Pixel XL', 'Device freezes during camera usage.', 'Cleared cache and updated camera app'),
('2021-12-17', 'OnePlus', 'One', 'Apps crash after update.', 'Cleared app cache and reinstalled updates'),
('2022-02-02', 'Huawei', 'Mate 20', 'Data connection is slow.', 'Reset network settings and checked SIM card'),
('2021-11-23', 'Xiaomi', 'Redmi Note 7', 'Keyboard input lag.', 'Cleared keyboard cache and reset settings');