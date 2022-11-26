odoo.define('gia_thanh.tinh_gia_thanh_tap_hop_khoan_giam_gia_thanh_don_hang_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var TapHopKhoanGiamGiaThanhDonHangFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        onViewLoaded: function(e, defer) {
            var self = this;
			var def =  defer;
            self.updateUI({'KY_TINH_GIA_THANH':self.params.tham_so});
            this.rpc_action({
                model: 'gia.thanh.tap.hop.khoan.giam.gia.thanh',
                method: 'lay_du_lieu_tap_hop_khoan_gia_thanh',
                args: {'ky_tinh_gia_thanh_id' : self.params.ky_tinh_gia_thanh_id},
                callback: function(result) {
                    if (result) {
                        self.updateUI(result);
                    }

                }
            });
			def.resolve();
        },
    });
    
    var TapHopKhoanGiamGiaThanhDonHangFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: TapHopKhoanGiamGiaThanhDonHangFormController,
        }),
    });
    
    view_registry.add('tinh_gia_thanh_tap_hop_khoan_giam_gia_thanh_don_hang_form_view', TapHopKhoanGiamGiaThanhDonHangFormView);
    
    return TapHopKhoanGiamGiaThanhDonHangFormView;
});
