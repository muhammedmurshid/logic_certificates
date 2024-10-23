odoo.define('logic_certificates.location', function (require) {
    'use strict';
    console.log('Initializing Location Module...');

    var FormController = require('web.FormController');
    var core = require('web.core');
    var _t = core._t;

    FormController.include({
        events: _.extend({}, FormController.prototype.events, {
            'click [data-action="getCurrentLocation"]': '_onGetCurrentLocation',
        }),

        /**
         * Handle the Get Current Location button click
         */
        _onGetCurrentLocation: async function () {
            console.log('Getting current location...');

            // Ensure that recordData is available
            if (!this.recordData || !this.recordData.id) {
                console.log('No record loaded, attempting to save...');

                // Attempt to save the record
                try {
                    await this.saveRecord();
                    console.log('Record saved successfully, trying to get location again...');

                    // Fetch the record again to ensure we have the updated data
                    await this._reloadRecord();

                    // Check if recordData is available after saving
                    if (this.recordData && this.recordData.id) {
                        console.log('Record ID is now available:', this.recordData.id);
                        return this._getLocation(); // Call the location method
                    } else {
                        console.error('Record ID is still not available after save.');
                    }
                } catch (error) {
                    console.error('Error saving the form:', error);
                    this.do_warn(
                        _t('Error'),
                        _t('Unable to save the form. Please save manually and try again.')
                    );
                }
                return; // Exit if the record is still not available
            }

            // If we reach here, we have a valid record ID
            console.log('Record ID found:', this.recordData.id);
            await this._getLocation(); // Get the location
        },

        _reloadRecord: async function () {
            const recordId = this.recordData.id;

            // Fetch the record data again to ensure we have the latest data
            const record = await this._rpc({
                model: 'logic.bonafide.certificates',
                method: 'read',
                args: [[recordId]],
            });

            // Assuming the record is found, update the recordData
            if (record && record.length) {
                this.recordData = record[0];
            } else {
                console.error('No record found for ID:', recordId);
            }
        },

        _getLocation: function () {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        const latitude = position.coords.latitude;
                        const longitude = position.coords.longitude;

                        console.log('Latitude:', latitude);
                        console.log('Longitude:', longitude);

                        // Prepare the updated data for the record
                        const locationData = {
                            latitude: latitude,
                            longitude: longitude,
                            // Assuming you have a field called 'location' where you want to store the coordinates
                            location: `${latitude}, ${longitude}`
                        };

                        // Call the Odoo RPC method to update the fields
                        this._rpc({
                            model: 'logic.bonafide.certificates',
                            method: 'write',
                            args: [[this.recordData.id], locationData]
                        }).then(() => {
                            console.log('Location updated:', locationData);
                            this.do_notify(
                                _t('Success'),
                                _t('Location updated successfully!')
                            );
                        }).catch((rpcError) => {
                            console.error('Error updating location:', rpcError);
                            this.do_warn(
                                _t('Error'),
                                _t('Unable to update location in the record.')
                            );
                        });
                    },
                    (error) => {
                        console.error('Error getting location', error);
                        this.do_warn(
                            _t('Error'),
                            _t('Unable to retrieve your location. Error: ' + error.message)
                        );
                    }
                );
            } else {
                this.do_warn(
                    _t('Error'),
                    _t('Geolocation is not supported by this browser.')
                );
            }
        },
    });
});
