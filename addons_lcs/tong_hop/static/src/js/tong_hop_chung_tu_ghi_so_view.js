odoo.define('tong_hop.tong_hop_chung_tu_ghi_so_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormRenderer = require('web.FormRenderer');
    var BasicModel = require('web.BasicModel');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var TongHopChungTuGhiSoController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },

        _onButtonClicked: function(event) {
            var self = this;
			event.stopPropagation();
            switch (event.data.attrs.id)
            {
                
                case "btn_chon_chung_tu":
                    var arr_chung_tu_da_chon = [];
                    var du_lieu = this.getLocalData();
                    var chung_tu_goc;
                    var id_goc;
                    if(du_lieu){
                        if(du_lieu.TONG_HOP_CHUNG_TU_GHI_SO_CHI_TIET_IDS.length > 0){
                            for(var i in du_lieu.TONG_HOP_CHUNG_TU_GHI_SO_CHI_TIET_IDS){
                                arr_chung_tu_da_chon.push({'id_chung_tu': du_lieu.TONG_HOP_CHUNG_TU_GHI_SO_CHI_TIET_IDS[0].ID_CHUNG_TU_GOC,
                                                           'model_goc' : du_lieu.TONG_HOP_CHUNG_TU_GHI_SO_CHI_TIET_IDS[0].MODEL_GOC
                                })
                            }
                        }
                    }
                    new dialogs.FormViewDialog(this, {
                        tham_so : arr_chung_tu_da_chon,
                        readonly: false,
                        res_model: 'tong.hop.ctgs.chon.chung.tu.form',
                        // size :'large',
                        ref_views: [['tong_hop.view_tong_hop_ctgs_chon_chung_tu_form_tham_so_form', 'form']],
                        title: ("Chọn chứng từ"),
                        disable_multiple_selection: true,
                        shouldSaveLocally: true,
                        on_after_saved: function (record, changed) {
                            if (changed) {
                                var dict_chi_tiet = [[5]];
                                var chi_tiet;
                                for(var i in record.data.TONG_HOP_CTGS_CHON_CHUNG_TU_CHI_TIET_FORM_IDS.data){
                                    chi_tiet = record.data.TONG_HOP_CTGS_CHON_CHUNG_TU_CHI_TIET_FORM_IDS.data[i].data;
                                    if (chi_tiet.AUTO_SELECT) {
                                        dict_chi_tiet.push([0, 0, {
                                            'NGAY_HACH_TOAN' : chi_tiet.NGAY_HACH_TOAN,
                                            'NGAY_CHUNG_TU' : chi_tiet.NGAY_CHUNG_TU,
                                            'SO_CHUNG_TU' : chi_tiet.SO_CHUNG_TU,
                                            'DIEN_GIAI' : chi_tiet.DIEN_GIAI,
                                            'TK_NO_ID' : [chi_tiet.TK_NO_ID.data.id,chi_tiet.TK_NO_ID.data.display_name],
                                            'TK_CO_ID' : [chi_tiet.TK_CO_ID.data.id,chi_tiet.TK_CO_ID.data.display_name],
                                            'SO_TIEN' : chi_tiet.SO_TIEN,
                                            'LOAI_CHUNG_TU' : chi_tiet.LOAI_CHUNG_TU,
                                            'ID_CHUNG_TU_GOC' : chi_tiet.ID_GOC,
                                            'MODEL_GOC' : chi_tiet.MODEL_GOC,
                                        }])
                                    }
                                }
                                self.updateUI({'TONG_HOP_CHUNG_TU_GHI_SO_CHI_TIET_IDS': dict_chi_tiet});
                            }
                        },
                    }).open();
                    break;

                default: 
                   this._super.apply(this, arguments);
            }
            
        }
    });

    var TongHopChungTuGhiSoRenderer = FormRenderer.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });

    var TongHopChungTuGhiSoModel = BasicModel.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });
    
    var TongHopChungTuGhiSoView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Model: TongHopChungTuGhiSoModel,
            Renderer: TongHopChungTuGhiSoRenderer,
            Controller: TongHopChungTuGhiSoController,
        }),
    });
    
    view_registry.add('tong_hop_chung_tu_ghi_so_view', TongHopChungTuGhiSoView);
    
    return TongHopChungTuGhiSoView;
});
