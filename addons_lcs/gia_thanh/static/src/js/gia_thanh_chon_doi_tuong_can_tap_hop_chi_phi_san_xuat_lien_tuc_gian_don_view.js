odoo.define('gia_thanh.chon_doi_tuong_can_tap_hop_chi_phi_san_xuat_lien_tuc_gian_don_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var ChonDoiTuongCanTapHopChiPhiSXLTGDFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        onViewLoaded: function(e, defer) {
            var self = this;
			var def =  defer;
			
            this.rpc_action({
                model: 'gia.thanh.chon.doi.tuong.can.tap.hop.chi.phi.form',
                method: 'lay_du_lieu_doi_tuong_thcp_hang_hoa_loai_san_pham',
                args: {},
                callback: function(result) {
                    if (result) {
                        self.updateUI(result);
                    }					
                }
            });
			def.resolve();
        },
    });
    
    var ChonDoiTuongCanTapHopChiPhiSXLTGDFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: ChonDoiTuongCanTapHopChiPhiSXLTGDFormController,
        }),
    });
    
    view_registry.add('chon_doi_tuong_can_tap_hop_chi_phi_san_xuat_lien_tuc_gian_don_form_view', ChonDoiTuongCanTapHopChiPhiSXLTGDFormView);
    
    return ChonDoiTuongCanTapHopChiPhiSXLTGDFormView;
});
