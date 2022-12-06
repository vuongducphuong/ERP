odoo.define('purchase_ex.tra_lai_hang_mua_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var TraLaiHangMuaController = FormController.extend({
        getPrintBlackList:function () {
            var blackList = {};
            if (this.getFieldValue('TRA_LAI_HANG_TRONG_KHO')== true) {
                if (this.getFieldValue('selection_chung_tu_mua_hang') == 'giam_tru_cong_no'){
                    blackList['01-TT: Phiếu thu'] = true;
                    blackList['01-TT: Phiếu thu (Mẫu 2 liên)'] = true;
                    blackList['01-TT: Phiếu thu (Mẫu A5)'] = true;
                } 
            }
            else{
                if (this.getFieldValue('selection_chung_tu_mua_hang') == 'giam_tru_cong_no'){
                    blackList['02-VT: Phiếu xuất kho'] = true;
                    blackList['02-VT: Phiếu xuất kho (Mẫu A5)'] = true;
                    blackList['01-TT: Phiếu thu'] = true;
                    blackList['01-TT: Phiếu thu (Mẫu 2 liên)'] = true;
                    blackList['01-TT: Phiếu thu (Mẫu A5)'] = true;
                }
                else if(this.getFieldValue('selection_chung_tu_mua_hang') == 'thu_tien_mat'){
                    blackList['02-VT: Phiếu xuất kho'] = true;
                    blackList['02-VT: Phiếu xuất kho (Mẫu A5)'] = true;
                }
            }
            return blackList;
        },
        onViewLoaded: function(e, defer) {
            var def = defer;
            this.changeSelectionSource('CHI_TIET_HANG_HOA', ['hang_tien']);
            if (def) {
                def.resolve();
            }
        },
        onFieldChanged: function(field){
            var self = this;
            var TRA_LAI_HANG_TRONG_KHO = this.getFieldValue('TRA_LAI_HANG_TRONG_KHO')
            var doi_tuong = this.getFieldValue('DOI_TUONG_ID')
            var doi_tuong_id;
            if (doi_tuong){
                doi_tuong_id = doi_tuong.id;
            }
            
            if (TRA_LAI_HANG_TRONG_KHO == true){
                this.changeSelectionSource('CHI_TIET_HANG_HOA', ['hang_tien']);
            }
            else{
                this.changeSelectionSource('CHI_TIET_HANG_HOA', ['hang_tien','thong_ke']);
            }
            if('DOI_TUONG_ID' == field){
                self.getFieldWidget('TK_NGAN_HANG_ID').changeDomain([['DOI_TUONG_ID','=',doi_tuong_id]]);
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
                    model: 'purchase.ex.tra.lai.hang.mua',
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
            } else if(field == 'DOI_TUONG_ID') {
                var domain = [];
                var field_value = this.getFieldValue(field);
                if (field_value) {
                    domain = [['DOI_TUONG_ID','=',field_value.id]]
                }
                this.getFieldWidget('CHUNG_TU_MUA_HANG').changeDomain(domain);
                this.getFieldWidget('CHUNG_TU_MUA_HANG_CHI_TIET').changeDomain(domain);
            }
                
        }
    });
    
    var TraLaiHangMuaView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: TraLaiHangMuaController,
        }),
    });
    
    view_registry.add('tra_lai_hang_mua_form_view', TraLaiHangMuaView);
    
    return TraLaiHangMuaView;
});

odoo.define('purchase_ex.tra_lai_hang_mua_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');

    var TraLaiHangMuaController = ListController.extend({
        getPrintBlackList:function () {
            var blackList = {};
            var selectedRecords = this.getSelectedRecords();
            for (var i=0; i<selectedRecords.length; i++) {
                var record = selectedRecords[i].data;
                if (record.TRA_LAI_HANG_TRONG_KHO == true) {
                    if (record.selection_chung_tu_mua_hang == 'giam_tru_cong_no'){
                        blackList['01-TT: Phiếu thu'] = true;
                        blackList['01-TT: Phiếu thu (Mẫu 2 liên)'] = true;
                        blackList['01-TT: Phiếu thu (Mẫu A5)'] = true;
                    } 
                }
                else{
                    if (record.selection_chung_tu_mua_hang == 'giam_tru_cong_no'){
                        blackList['02-VT: Phiếu xuất kho'] = true;
                        blackList['02-VT: Phiếu xuất kho (Mẫu A5)'] = true;
                        blackList['01-TT: Phiếu thu'] = true;
                        blackList['01-TT: Phiếu thu (Mẫu 2 liên)'] = true;
                        blackList['01-TT: Phiếu thu (Mẫu A5)'] = true;
                    }
                    else if(record.selection_chung_tu_mua_hang == 'thu_tien_mat'){
                        blackList['02-VT: Phiếu xuất kho'] = true;
                        blackList['02-VT: Phiếu xuất kho (Mẫu A5)'] = true;
                    }
                }
            }
            return blackList;
        },
    });
    
    var TraLaiHangMuaView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: TraLaiHangMuaController,
        }),
    });
    
    view_registry.add('tra_lai_hang_mua_list_view', TraLaiHangMuaView);
    
    return TraLaiHangMuaView;
});