odoo.define('tong_hop.tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var PhanBoChiPhiBHQLDNChiPhiDonViController = FormController.extend({
        onViewLoaded: function(e, defer) {
            var phan_bo = this.getFieldValue('PHAN_BO_SELECTION_LAY_DU_LIEU');
            if (phan_bo == 'PHAN_BO_CHO_DON_VI') {
                this.changeSelectionSource('TIEU_THUC_PHAN_BO_ALL', ['1'])
            } else {
                this.changeSelectionSource('TIEU_THUC_PHAN_BO_ALL')
            }
			defer.resolve()
        },

        _onCreate: function () {
            var self = this;
            new dialogs.FormParamsDialog(this, _.extend({}, this.nodeOptions, {
                res_model: 'tong.hop.chon.ky.phan.bo.chi.phi',
                title: 'Chọn kỳ phân bổ chi phí',
                ref_views: [['tong_hop.view_tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi_form', 'form']],
                on_selected: function (params,handle) {
                    var context = {
                        'default_TU_NGAY': params.TU_NGAY,
                        'default_DEN_NGAY': params.DEN_NGAY,
                        'default_PHAN_BO': params.PHAN_BO_SELECTION,
                        
                    }
                    self.createRecord(context);
                    self.closeDialog(handle);
                },
            })).open();
        },

        _onButtonClicked: function(event) {
            var self = this;
			event.stopPropagation();
            switch (event.data.attrs.id)
            {
                
                case "btn_chon_doi_tuong_phan_bo":
                    return new dialogs.SelectParamsDialog(this, _.extend({}, this.nodeOptions, {
                        res_model: 'tong.hop.phan.bo.chon.doi.tuong.phan.bo.form',
                        title: 'Chọn đối tượng phân bổ',
                        ref_views: [['tong_hop.view_tong_hop_phan_bo_chon_doi_tuong_phan_bo_form_tham_so_form', 'form']],
                        // context: _.extend(event.data.record.context || {}, event.data.record.data || {}),
                        on_selected: function () {
                           
                            
                        },
                    })).open();
					break;

                default: 
                   this._super.apply(this, arguments);
            }
            
        }
    });
    
    var PhanBoChiPhiBHQLDNChiPhiDonViView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: PhanBoChiPhiBHQLDNChiPhiDonViController,
        }),
    });
    
    view_registry.add('tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi_view', PhanBoChiPhiBHQLDNChiPhiDonViView);
    
    return PhanBoChiPhiBHQLDNChiPhiDonViView;
});

odoo.define('tong_hop.tong_hop_kiem_ke_bang_kiem_ke_vat_tu_hang_hoa_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var PhanBoChiPhiBHQLDNChiPhiDonViController = ListController.extend({
        _onCreate: function() {
            var self = this;
            new dialogs.FormParamsDialog(this, _.extend({}, this.nodeOptions, {
                res_model: 'tong.hop.chon.ky.phan.bo.chi.phi',
                title: 'Chọn kỳ phân bổ chi phí',
                ref_views: [['tong_hop.view_tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi_form', 'form']],
                on_selected: function (params,handle) {
                    var context = {
                        'default_TU_NGAY': params.TU_NGAY,
                        'default_DEN_NGAY': params.DEN_NGAY,
                        'default_PHAN_BO': params.PHAN_BO_SELECTION,
                        
                    }
                    self.createRecord(context);
                    self.closeDialog(handle);
                },
            })).open();
            
        },
    });
    
    var PhanBoChiPhiBHQLDNChiPhiDonViView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: PhanBoChiPhiBHQLDNChiPhiDonViController,
        }),
    });
    
    view_registry.add('tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi_list_view', PhanBoChiPhiBHQLDNChiPhiDonViView);
    
    return PhanBoChiPhiBHQLDNChiPhiDonViView;

});
