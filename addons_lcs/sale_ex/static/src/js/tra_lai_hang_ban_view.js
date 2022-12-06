odoo.define('sale_ex.tra_lai_hang_ban_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var TraLaiHangBanController = FormController.extend({
        getPrintBlackList:function () {
            var blackList = {};
            
            if (this.getFieldValue('selection_chung_tu_ban_hang') == 'giam_tru_cong_no'){
                blackList['02-TT:Phiếu chi'] = true;
                blackList['02-TT:Phiếu chi (Mẫu 2 liên)'] = true;
                blackList['02-TT:Phiếu chi (Mẫu A5)'] = true;

            }
            if (this.getFieldValue('KIEM_TRA_PHIEU_NHAP_KHO') == false){
                blackList['01-VT:Phiếu nhập kho'] = true;
                blackList['01-VT:Phiếu nhập kho (Mẫu A5)'] = true;
            }
            
            return blackList;
        },
        onFieldChanged: function(field){
            var self = this;
            if (field == 'KIEM_TRA_PHIEU_NHAP_KHO' || field == 'CHUNG_TU_HANG_BAN_BI_TRA_LAI') {
                var KIEM_TRA_PHIEU_NHAP_KHO = this.getFieldValue('KIEM_TRA_PHIEU_NHAP_KHO')
                var CHUNG_TU_HANG_BAN_BI_TRA_LAI = this.getFieldValue('CHUNG_TU_HANG_BAN_BI_TRA_LAI')
                if (CHUNG_TU_HANG_BAN_BI_TRA_LAI == 'BAN_HANG_HOA_DICH_VU'){
                    if (KIEM_TRA_PHIEU_NHAP_KHO == true){
                        this.changeSelectionSource('chi_tiet', ['hang_tien','thue','gia_von','thong_ke']);
                    }
                    else{
                        this.changeSelectionSource('chi_tiet', ['hang_tien','thue','thong_ke']);
                    }

                }
                else if(CHUNG_TU_HANG_BAN_BI_TRA_LAI == 'BAN_HANG_DAI_LY_BAN_DUNG_GIA'){
                    if (KIEM_TRA_PHIEU_NHAP_KHO == true){
                        this.changeSelectionSource('chi_tiet', ['hang_tien','thue','gia_von','thong_ke']);
                    }
                    else{
                        this.changeSelectionSource('chi_tiet', ['hang_tien','thue','thong_ke']);
                    }
                }
                else if(CHUNG_TU_HANG_BAN_BI_TRA_LAI == 'BAN_HANG_UY_THAC_XUAT_KHAU'){
                    if (KIEM_TRA_PHIEU_NHAP_KHO == true){
                        this.changeSelectionSource('chi_tiet', ['hang_tien','gia_von','thong_ke']);
                    }
                    else{
                        this.changeSelectionSource('chi_tiet', ['hang_tien','thong_ke']);
                    }
                }
            }
            else if(field == 'CHUNG_TU_BAN_HANG'){
                var CHUNG_TU_BAN_HANG = this.getFieldValue('CHUNG_TU_BAN_HANG')
                var id_ctbh;
                var name_ctbh;
                if (CHUNG_TU_BAN_HANG){
                    id_ctbh =  CHUNG_TU_BAN_HANG.id;
                    name_ctbh = CHUNG_TU_BAN_HANG.display_name;
                }
                this.rpc_action({
                    model: 'sale.ex.tra.lai.hang.ban',
                    method: 'lay_du_lieu_chung_tu_ban_hang',
                    args: {
                        'chung_tu_ban_hang_id' :id_ctbh,
                        'chung_tu_ban_hang_name' : name_ctbh,
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
                this.getFieldWidget('CHUNG_TU_BAN_HANG').changeDomain(domain);
                this.getFieldWidget('CHUNG_TU_BAN_HANG_CHI_TIET').changeDomain(domain);
            }
        }
    });
    
    var TraLaiHangBanView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: TraLaiHangBanController,
        }),
    });
    
    view_registry.add('tra_lai_hang_ban_form_view', TraLaiHangBanView);
    
    return TraLaiHangBanView;
});

odoo.define('sale_ex.tra_lai_hang_ban_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');

    var TraLaiHangBanController = ListController.extend({
        getPrintBlackList:function () {
            var blackList = {};
            var selectedRecords = this.getSelectedRecords();
            for (var i=0; i<selectedRecords.length; i++) {
                var record = selectedRecords[i].data;
                if (record.selection_chung_tu_ban_hang == 'giam_tru_cong_no'){
                    blackList['02-TT:Phiếu chi'] = true;
                    blackList['02-TT:Phiếu chi (Mẫu 2 liên)'] = true;
                    blackList['02-TT:Phiếu chi (Mẫu A5)'] = true;
    
                }
                if (record.KIEM_TRA_PHIEU_NHAP_KHO == false){
                    blackList['01-VT:Phiếu nhập kho'] = true;
                    blackList['01-VT:Phiếu nhập kho (Mẫu A5)'] = true;
                }
            }
            return blackList;
        },
    });
    
    var TraLaiHangBanView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: TraLaiHangBanController,
        }),
    });
    
    view_registry.add('tra_lai_hang_ban_list_view', TraLaiHangBanView);
    
    return TraLaiHangBanView;
});