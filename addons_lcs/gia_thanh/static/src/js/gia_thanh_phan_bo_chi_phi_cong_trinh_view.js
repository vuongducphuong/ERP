odoo.define('gia_thanh.tinh_gia_thanh_phan_bo_chi_phi_cong_trinh_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var PhanBoChiPhiCongTrinhFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        onViewLoaded: function(e, defer) {
            var self = this;
			var def =  defer;
			self.updateUI({'KY_TINH_GIA_THANH':self.params.tham_so,'KY_TINH_GIA_THANH_ONCHANGE':self.params.ky_tinh_gia_thanh_id,'LOAI_TINH_GIA_THANH' : 'CONG_TRINH'});
			self.rpc_action({
                model: 'gia.thanh.tinh.gia.thanh',
                method: 'lay_du_lieu_tinh_gia_thanh_sx_lien_tuc',
                args: {},
                callback: function(result) {
                    if (result) {
                        self.updateUI(result);
                    }
									
                }
            });
			def.resolve();
        },
        _onButtonClicked: function(event) {
            event.stopPropagation();
            var def = $.Deferred();
            var self = this;
            // var HANG_MUC =  this.getFieldValue('HANG_MUC');
            switch (event.data.attrs.id)
            {
                case "btn_phan_bo":
                    var bien_tam = self.getFieldValue('ONCHANGE_CLICK_PHAN_BO')
                    self.changeFieldValue('ONCHANGE_CLICK_PHAN_BO',bien_tam + 1);
                    break;
                case "btn_luu":
                    this.rpc_action({
                        model: 'gia.thanh.tinh.gia.thanh',
                        method: 'luu_tinh_gia_thanh',
                        callback: function(result) {
                            self.do_notify('Thông báo', 'Lưu dữ liệu thành công',true);
                            self.closeDialog();
                            
                        }
                    });
                    break;
                default: 
                this._super.apply(this, arguments);
             }
             
         },

         onRowChanged: function(field, columnName, newValue, recordValue, record) {
            if(field == 'GIA_THANH_XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET_IDS'){
                if (columnName == 'SO_PHAN_BO_LAN_NAY' || columnName == 'PHAN_TRAM_PB_LAN_NAY') {
                    var chung_tu_phan_bo_chi_phi_chung_ids = this.getFieldValue('GIA_THANH_CHI_TIET_CHUNG_TU_PHAN_BO_CHI_PHI_CHUNG_IDS');
                    var tong_tien_phan_bo_lan_nay = recordValue.SO_PHAN_BO_LAN_NAY;
                    var phan_tram_phan_bo_lan_nay = recordValue.PHAN_TRAM_PB_LAN_NAY;
                    var tai_khoan = false;
                    if(this.model.localData[recordValue.TAI_KHOAN_ID]){
                        tai_khoan = this.model.localData[recordValue.TAI_KHOAN_ID].data.id;
                    }
                    var update_list = {
                        'GIA_THANH_CHI_TIET_CHUNG_TU_PHAN_BO_CHI_PHI_CHUNG_IDS': [],
                    }
                    for(var i=0;i<chung_tu_phan_bo_chi_phi_chung_ids.length;i++){
                        var chi_tiet = chung_tu_phan_bo_chi_phi_chung_ids[i];
                        if(chi_tiet.TK_CHI_PHI_ID.id == tai_khoan){
                            var ty_le_phan_bo = 0;
                            if(chi_tiet.SO_CHUA_PHAN_BO < tong_tien_phan_bo_lan_nay && chi_tiet.SO_CHUA_PHAN_BO > 0){
                                if(chi_tiet.SO_CHUA_PHAN_BO > 0){
                                    ty_le_phan_bo = phan_tram_phan_bo_lan_nay;
                                }
                                update_list['GIA_THANH_CHI_TIET_CHUNG_TU_PHAN_BO_CHI_PHI_CHUNG_IDS'].push([1, chi_tiet.res_id, { 'SO_PHAN_BO_LAN_NAY': chi_tiet.SO_CHUA_PHAN_BO,'TY_LE_PHAN_BO' : ty_le_phan_bo}]);
                                tong_tien_phan_bo_lan_nay = tong_tien_phan_bo_lan_nay - chi_tiet.SO_CHUA_PHAN_BO;
                            }
                            else{
                                if(chi_tiet.SO_CHUA_PHAN_BO > 0){
                                    ty_le_phan_bo = phan_tram_phan_bo_lan_nay;
                                }
                                update_list['GIA_THANH_CHI_TIET_CHUNG_TU_PHAN_BO_CHI_PHI_CHUNG_IDS'].push([1, chi_tiet.res_id, { 'SO_PHAN_BO_LAN_NAY': tong_tien_phan_bo_lan_nay,'TY_LE_PHAN_BO' : ty_le_phan_bo }]);
                                tong_tien_phan_bo_lan_nay = 0;
                            }
                            this.updateUI(update_list);
                        }
                        
                    }
                    
                }
            }
            
            return true;
        },
    });
    
    var PhanBoChiPhiCongTrinhFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: PhanBoChiPhiCongTrinhFormController,
        }),
    });
    
    view_registry.add('tinh_gia_thanh_phan_bo_chi_phi_cong_trinh_form_view', PhanBoChiPhiCongTrinhFormView);
    
    return PhanBoChiPhiCongTrinhFormView;
});
