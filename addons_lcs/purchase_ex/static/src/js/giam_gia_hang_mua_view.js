odoo.define('purchase_ex.giam_gia_hang_mua_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var GiamGiaHangMuaController = FormController.extend({
        getPrintBlackList:function () {
            var blackList = {};
            if (this.getFieldValue('selection_chung_tu_giam_gia_hang_mua') == 'giam_tru_cong_no'){
                blackList['01-TT: Phiếu thu'] = true;
                blackList['01-TT: Phiếu thu (Mẫu 2 liên)'] = true;
                blackList['01-TT: Phiếu thu (Mẫu A5)'] = true;
            }     
            return blackList;
        },
        onViewLoaded: function(e, defer) {
            var def = defer;
            this.getFieldWidget('CHUNG_TU_MUA_HANG').changeDomain(['|',['LOAI_CHUNG_TU_MH','=','trong_nuoc_nhap_kho'],['LOAI_CHUNG_TU_MH','=','nhap_khau_nhap_kho']]);
            this.changeSelectionSource('CHI_TIET_HANG_HOA', ['hang_tien']);
            if (def) {
                def.resolve();
            }
        },

        onFieldChanged: function(field){
            var self = this;
            if (field == 'GIAM_GIA_TRI_HANG_NHAP_KHO'){
                var GIAM_GIA_TRI_HANG_NHAP_KHO = this.getFieldValue('GIAM_GIA_TRI_HANG_NHAP_KHO')
                if (GIAM_GIA_TRI_HANG_NHAP_KHO == true){
                    this.changeSelectionSource('CHI_TIET_HANG_HOA', ['hang_tien']);
                    self.getFieldWidget('CHUNG_TU_MUA_HANG').changeDomain(['|',['LOAI_CHUNG_TU_MH','=','trong_nuoc_nhap_kho'],['LOAI_CHUNG_TU_MH','=','nhap_khau_nhap_kho']]);
                }
                else{
                    this.changeSelectionSource('CHI_TIET_HANG_HOA', ['hang_tien','thong_ke']);
                    self.getFieldWidget('CHUNG_TU_MUA_HANG').changeDomain(['|',['LOAI_CHUNG_TU_MH','=','trong_nuoc_khong_qua_kho'],['LOAI_CHUNG_TU_MH','=','nhap_khau_khong_qua_kho']]);
                }
            }
            if(field == 'CHUNG_TU_MUA_HANG'){
                var CHUNG_TU_MUA_HANG = this.getFieldValue('CHUNG_TU_MUA_HANG')
                var id_ctmh;
                var name_ctmh;
                if (CHUNG_TU_MUA_HANG){
                    id_ctmh =  CHUNG_TU_MUA_HANG.id;
                    name_ctmh = CHUNG_TU_MUA_HANG.display_name;
                }
                this.rpc_action({
                    model: 'purchase.ex.giam.gia.hang.mua',
                    method: 'lay_du_lieu_chung_tu_mua_hang',
                    args: {
                        'chung_tu_mua_hang_id' :id_ctmh,
                        'chung_tu_mua_hang_name' : name_ctmh,
                    },
                    callback: function(result) {
                        if (result) {
                            self.updateUI(result);
                        }
                    }
                });
            }    
        }
    });
    
    var GiamGiaHangMuaView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: GiamGiaHangMuaController,
        }),
    });
    
    view_registry.add('giam_gia_hang_mua_form_view', GiamGiaHangMuaView);
    
    return GiamGiaHangMuaView;
});

odoo.define('purchase_ex.giam_gia_hang_mua_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');

    var GiamGiaHangMuaController = ListController.extend({
        getPrintBlackList:function () {
            var blackList = {};
            var selectedRecords = this.getSelectedRecords();
            for (var i=0; i<selectedRecords.length; i++) {
                var record = selectedRecords[i].data;
                if (record.selection_chung_tu_giam_gia_hang_mua == 'giam_tru_cong_no'){
                    blackList['01-TT: Phiếu thu'] = true;
                    blackList['01-TT: Phiếu thu (Mẫu 2 liên)'] = true;
                    blackList['01-TT: Phiếu thu (Mẫu A5)'] = true;
                }
            }
            return blackList;
        },
    });
    
    var GiamGiaHangMuaView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: GiamGiaHangMuaController,
        }),
    });
    
    view_registry.add('giam_gia_hang_mua_list_view', GiamGiaHangMuaView);
    
    return GiamGiaHangMuaView;
});