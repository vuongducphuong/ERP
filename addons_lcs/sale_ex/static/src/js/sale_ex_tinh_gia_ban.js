odoo.define('sale_ex.tinh_gia_ban_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var TinhGiaBanFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },

        onViewLoaded: function(e, defer) {
            var self = this;
            $('#btn_hoan').attr('disabled', true);
			if (defer) {
				defer.resolve();
			}
            // this.rpc_action({
            //     model: 'sale.ex.tinh.gia.ban',
            //     // method: 'lay_chung_tu_luu_ma_quy_cach',
            //     // args: {},
                   
            //     callback: function(result) {
            //         if (result) {
            //             self.updateUI(result);
            //         }
                    
            //     }
            // });
        },

        _onButtonClicked: function(event) {
            var self = this;
			event.stopPropagation();
            switch (event.data.attrs.id)
            {
                
                case "btn_tinh_gia_ban":
                    this.rpc_action({
                        model: 'sale.ex.tinh.gia.ban',
                        method: 'tinh_gia_ban',
                        // args: {},
                        callback: function(result) {
                            self.updateUI(result);
                            $('#btn_hoan').attr('disabled', false);
                            $('#btn_tinh_gia_ban').attr('disabled', true);
                        }
                    });
                    
                    break;

                case "btn_hoan":
                    this.rpc_action({
                        model: 'sale.ex.tinh.gia.ban',
                        method: 'xu_ly_hoan',
                        // args: {},
                        callback: function(result) {
                            self.updateUI(result);
                            $('#btn_hoan').attr('disabled', true);
                            $('#btn_tinh_gia_ban').attr('disabled', false);
                        }
                    })
                    break;

                default: 
                   this._super.apply(this, arguments);
            };

            if (event.data.attrs.class.includes("o_form_button_save"))
            {
                $('#btn_hoan').attr('disabled', true);
                // this.rpc_action({
                //     model: 'sale.ex.tinh.gia.ban',
                //     method: 'tinh_gia_ban',
                //     // args: {},
                //     callback: function(result) {
                //         self.updateUI(result);
                //         $('#btn_hoan').attr('disabled', false);
                //         $('#btn_tinh_gia_ban').attr('disabled', true);
                //     }
                // });
                    
            }
            
        }

    });
    
    var TinhGiaBanFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: TinhGiaBanFormController,
        }),
    });
    
    view_registry.add('tinh_gia_ban_form_view', TinhGiaBanFormView);
    
    return TinhGiaBanFormView;
});
