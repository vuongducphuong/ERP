odoo.define('account_ex.account_ex_don_dat_hang_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var DonDatHangController = FormController.extend({

        _onButtonClicked: function(event) {
            var self = this;
			event.stopPropagation();
            switch (event.data.attrs.class)
            {
                case "btn_xem_sl_ton":
                   return new dialogs.SelectParamsDialog(this, _.extend({}, this.nodeOptions, {
                        res_model: 'account.ex.don.dat.hang.xem.sl.ton.chua.dat.hang.form',
                        title: 'Danh sách số lượng tồn chưa đặt hàng',
                        ref_views: [['account_ex.view_account_ex_don_dat_hang_xem_sl_ton_chua_dat_hang_form_form', 'form']],
                        // context: _.extend(event.data.record.context || {}, event.data.record.data || {}),
                        on_selected: function (records) {
                           
                        }, 
                    })).open();
                    
                    case "btn_xem_cong_no":
                        self.rpc_action({
                            model: 'account.ex.don.dat.hang',
                            method: 'btn_xem_cong_no',
                            callback: function (result) {
                                if (result) {
                                    Dialog.show_message('Công nợ khách hàng', result, 'ALERT');
                                }
                            }
                        });
                        break;
                
                default: 
                   this._super.apply(this, arguments);
            }
            
        }
    });
    
    var DonDatHangView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: DonDatHangController,
        }),
    });
    
    view_registry.add('account_ex_don_dat_hang_view', DonDatHangView);
    
    return DonDatHangView;
});
