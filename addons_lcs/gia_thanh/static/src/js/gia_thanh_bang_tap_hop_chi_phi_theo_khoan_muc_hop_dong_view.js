odoo.define('gia_thanh.tinh_gia_thanh_bang_tap_hop_chi_phi_theo_khoan_muc_hop_dong_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var TapHopChiPhiTheoKhoanMucHopDongFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        onViewLoaded: function(e, defer) {
            var self = this;
			var def =  defer;
            self.updateUI({'KY_TINH_GIA_THANH':self.params.tham_so});
            this.rpc_action({
                model: 'gia.thanh.bang.tap.hop.chi.phi.theo.khoan.muc',
                method: 'btn_chi_phi_theo_khoan_muc_ct_dh_hd',
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
    
    var TapHopChiPhiTheoKhoanMucHopDongFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
           
            Controller: TapHopChiPhiTheoKhoanMucHopDongFormController,
        }),
    });
    
    view_registry.add('tinh_gia_thanh_bang_tap_hop_chi_phi_theo_khoan_muc_hop_dong_form_view', TapHopChiPhiTheoKhoanMucHopDongFormView);
    
    return TapHopChiPhiTheoKhoanMucHopDongFormView;
});
