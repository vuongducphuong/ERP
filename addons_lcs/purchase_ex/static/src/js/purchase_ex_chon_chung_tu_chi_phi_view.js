odoo.define('purchase_ex.chon_chung_tu_chi_phi_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var ChonChungTuChiPhiController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },

        _onButtonClicked: function(event) {
            var self = this;
			event.stopPropagation();
            switch (event.data.attrs.id)
            {
                
                case "btn_lay_du_lieu":
                    var id_chung_tu = this.params.tham_so[0];
                    var arr_chung_tu_da_chon = this.params.tham_so[1];
                    var doi_tuong = -1;
                    if(self.getFieldValue('DOI_TUONG_ID') != null){
                        doi_tuong = self.getFieldValue('DOI_TUONG_ID').id
                    }
                    
                    this.rpc_action({
                        model: 'purchase.ex.chon.chung.tu.chi.phi',
                        method: 'lay_du_lieu_chung_tu',
                        args: {
                            'doi_tuong_id' : doi_tuong,
                            'tu_ngay' : self.getFieldValue('TU_NGAY'),
                            'den_ngay' : self.getFieldValue('DEN_NGAY'),
                            'id_chung_tu' : id_chung_tu,
                            'arr_chung_tu_da_chon' : arr_chung_tu_da_chon,
                        },
                        callback: function(result) {
                            if (result) {
                                self.updateUI({'PURCHASE_EX_CHON_CHUNG_TU_CHI_PHI_CHI_TIET_IDS': result});
                            }
                        }
                    });
					break;

                default: 
                   this._super.apply(this, arguments);
            }
            
        }
    });

    
    var ChonChungTuChiPhiView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: ChonChungTuChiPhiController,
        }),
    });
    
    view_registry.add('chon_chung_tu_chi_phi_view', ChonChungTuChiPhiView);
    
    return ChonChungTuChiPhiView;
});
