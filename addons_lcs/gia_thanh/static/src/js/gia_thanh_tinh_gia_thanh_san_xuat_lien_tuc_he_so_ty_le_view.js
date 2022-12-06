odoo.define('gia_thanh.tinh_gia_thanh_san_xuat_lien_tuc_he_so_ty_le_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var TinhGiaThanhSanXuatLienTucHeSoTyLeFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        onViewLoaded: function(e, defer) {
            var self = this;
			var def =  defer;
			self.updateUI({'KY_TINH_GIA_THANH':self.params.tham_so});
            self.changeFieldValue('KY_TINH_GIA_THANH_ONCHANGE',self.params.ky_tinh_gia_thanh_id);
            self.changeFieldValue('TU_NGAY',self.params.tu_ngay);
            self.changeFieldValue('DEN_NGAY',self.params.den_ngay);
            self.changeFieldValue('LOAI_TINH_GIA_THANH',self.params.loai_tinh_gia_thanh);
            this.rpc_action({
                model: 'gia.thanh.tinh.gia.thanh',
                method: 'lay_du_lieu_tinh_gia_thanh_sx_lien_tuc',
                args: {'ky_tinh_gia_thanh_id' : self.params.ky_tinh_gia_thanh_id},
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
            var error= []; 
            var self = this;
            var HANG_MUC =  this.getFieldValue('HANG_MUC');
            switch (event.data.attrs.id)
            {
                
                case "btn_quay_lai":
                    if (HANG_MUC == 'TINH_GIA_THANH'){
                        self.changeFieldValue('HANG_MUC', 'XD_TY_LE_PHAN_BO');
                    }
                    else if (HANG_MUC == 'XD_TY_LE_PHAN_BO'){
                        self.changeFieldValue('HANG_MUC', 'DANH_GIA_DO_DANG');
                    }
                    else if (HANG_MUC == 'DANH_GIA_DO_DANG'){
                        self.changeFieldValue('HANG_MUC', 'PHAN_BO_CP_CHUNG');
                    }
                    break;
                case "btn_tiep_theo":
                    if (HANG_MUC == 'PHAN_BO_CP_CHUNG'){
                        this.rpc_action({
                            model: 'gia.thanh.tinh.gia.thanh',
                            method: 'validate_tien_phan_bo',
                            callback: function(result) {
                                if (result) {
                                    if(result.loi == true){
                                        Dialog.show_message('Thông báo', result.thong_bao, 'ALERT')
                                        .then(function(result) {
                                            return
                                        });
                                    }else{
                                        self.changeFieldValue('HANG_MUC', 'DANH_GIA_DO_DANG');
                                    }
                                }
                            }
                        });
                        // var tong_so_tien_da_phan_bo = this.getFieldValue('TONG_SO_DA_PHAN_BO');
                        // var tong_so_tien_chi_phi = this.getFieldValue('TONG_SO_CHI_PHI');
                        // if (tong_so_tien_da_phan_bo != tong_so_tien_chi_phi){
                        //     error = 'Tổng số tiền phân bổ của TK <6277> cho các đối tượng THCP phải bằng số phân bổ lần này của TK đó. Vui lòng kiểm tra lại.';
                        //     if (error.length) {
                        //         self.notifyInvalidFields(error);
                        //         def.resolve(false);
                        //     } else {
                        //         def.resolve(true);
                        //     }
                        //     return def;  
                        // }
                        // else{
                        //     self.changeFieldValue('HANG_MUC', 'DANH_GIA_DO_DANG');
                        // }
                    }
                    else if (HANG_MUC == 'DANH_GIA_DO_DANG'){
                        self.changeFieldValue('HANG_MUC', 'XD_TY_LE_PHAN_BO');
                    }
                    break;
                case "btn_tinh_gia_thanh":
                    self.changeFieldValue('HANG_MUC', 'TINH_GIA_THANH');
                    var bien_tam = self.getFieldValue('ONCHANGE_CLICK_TINH_GIA_THANH')
                    self.changeFieldValue('ONCHANGE_CLICK_TINH_GIA_THANH',bien_tam + 1);
                    break;
                case "btn_phan_bo":
                    var bien_tam = self.getFieldValue('ONCHANGE_CLICK_PHAN_BO')
                    self.changeFieldValue('ONCHANGE_CLICK_PHAN_BO',bien_tam + 1);
//                     self.changeFieldValue('KY_TINH_GIA_THANH_ONCHANGE',self.params.ky_tinh_gia_thanh_id);
                    break;
                case "btn_tinh_cap_nhat_gia_nhap_kho":
                    var bien_tam = self.getFieldValue('ONCHANGE_CLICK_CAP_NHAT_GIA_NHAP_KHO')
                    // self.changeFieldValue('ONCHANGE_CLICK_CAP_NHAT_GIA_NHAP_KHO',bien_tam + 1);
                    self.updateUI({'ONCHANGE_CLICK_CAP_NHAT_GIA_NHAP_KHO': bien_tam + 1}).then(function() {
                           self.do_notify('Thông báo', 'Cập nhật giá nhập kho thành công',true);
                    }); 
                    break;
                case "btn_tinh_cap_nhat_gia_xuat_kho":
                    var bien_tam = self.getFieldValue('ONCHANGE_CLICK_CAP_NHAT_GIA_XUAT_KHO')
//                     self.changeFieldValue('ONCHANGE_CLICK_CAP_NHAT_GIA_XUAT_KHO',bien_tam + 1);
                    self.updateUI({'ONCHANGE_CLICK_CAP_NHAT_GIA_XUAT_KHO': bien_tam + 1}).then(function() {
                           self.do_notify('Thông báo', 'Cập nhật giá xuất kho thành công',true);
                    }); 
                    break;
                case "btn_tinh_cp_do_dang":
                    var bien_tam = self.getFieldValue('ONCHANGE_CLICK_TINH_CP_DD')
                    self.changeFieldValue('ONCHANGE_CLICK_TINH_CP_DD',bien_tam + 1);
//                     self.changeFieldValue('KY_TINH_GIA_THANH_ONCHANGE',self.params.ky_tinh_gia_thanh_id);
                    break;
                case "btn_lay_gia_thanh_dinh_muc":
                    var bien_tam = self.getFieldValue('ONCHANGE_CLICK_LAY_GIA_THANH_DINH_MUC')
                    self.changeFieldValue('ONCHANGE_CLICK_LAY_GIA_THANH_DINH_MUC',bien_tam + 1);
                    break;
                case "btn_luu":
                    this.rpc_action({
                        model: 'gia.thanh.tinh.gia.thanh',
                        method: 'luu_tinh_gia_thanh',
                        callback: function() {
                            self.do_notify('Thông báo', 'Lưu dữ liệu thành công',true);
                            self.closeDialog();
                        }
                    });
                    break;
                // case "btn_tinh_ty_le_phan_bo":
                //     break;
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

        onRowChanged: function(field, columnName, newValue, recordValue, record) {
            if(field == 'GIA_THANH_XAC_DINH_TY_LE_PHAN_BO_DOI_TUONG_TINH_GIA_THANH_CHI_TIET_IDS'){
                if (columnName == 'HE_SO' || columnName == 'SO_LUONG_THANH_PHAM_CHUAN') {
                    var dict_tinh_tong = {};
                    var chung_tu_chi_tiet = this.getFieldValue('GIA_THANH_XAC_DINH_TY_LE_PHAN_BO_DOI_TUONG_TINH_GIA_THANH_CHI_TIET_IDS');
                    for(var i = 0;i<chung_tu_chi_tiet.length;i++){
                        var chi_tiet = chung_tu_chi_tiet[i];
                        if((chi_tiet.DOI_TUONG_THCP_ID.id in dict_tinh_tong) == false){
                            dict_tinh_tong[chi_tiet.DOI_TUONG_THCP_ID.id] = 0
                            
                        }
                        dict_tinh_tong[chi_tiet.DOI_TUONG_THCP_ID.id] += chi_tiet.SO_LUONG_THANH_PHAM_CHUAN*chi_tiet.HE_SO;
                    };
                    for(var i = 0;i<chung_tu_chi_tiet.length;i++){ 
                        var chi_tiet = chung_tu_chi_tiet[i];
                            
                        if(chi_tiet.DOI_TUONG_THCP_ID.id in dict_tinh_tong){
                            var tong_ty_le_phan_bo = dict_tinh_tong[chi_tiet.DOI_TUONG_THCP_ID.id];
                            var ty_le_phan_bo = (chi_tiet.SO_LUONG_THANH_PHAM_CHUAN/tong_ty_le_phan_bo)*100;
                            this.updateUI({ 'GIA_THANH_XAC_DINH_TY_LE_PHAN_BO_DOI_TUONG_TINH_GIA_THANH_CHI_TIET_IDS': [[1, chi_tiet.res_id, { 'TY_LE_PHAN_BO_GIA_THANH': ty_le_phan_bo }]] });
                        }
                        
                    }
                }
            };
            // if(field == 'GIA_THANH_TY_LE_PHAN_BO_DOI_TUONG_THCP_CHI_TIET_IDS'){
            //     if(columnName == "PHUONG_PHAP_XAC_DINH"){
            //         var phuong_phap_xac_minh = recordValue.PHUONG_PHAP_XAC_DINH;
            //         if(phuong_phap_xac_minh == 'TY_LE'){
            //             var fieldWidget = this.getFieldWidget('GIA_THANH_XAC_DINH_TY_LE_PHAN_BO_DOI_TUONG_TINH_GIA_THANH_CHI_TIET_IDS');
            //             fieldWidget.do_visible_columns(['LA_THANH_PHAM_CHUAN','HE_SO'], false);
            //             fieldWidget.do_visible_columns(['TIEU_CHUAN_PHAN_BO','HE_SO'], true);
            //         }else{
            //             var fieldWidget = this.getFieldWidget('GIA_THANH_XAC_DINH_TY_LE_PHAN_BO_DOI_TUONG_TINH_GIA_THANH_CHI_TIET_IDS');
            //             fieldWidget.do_visible_columns(['LA_THANH_PHAM_CHUAN','HE_SO'], true);
            //             fieldWidget.do_visible_columns(['TIEU_CHUAN_PHAN_BO','HE_SO'], false);
            //         }
            //     }
            // }
            
            return true;
        },
    });
    
    var TinhGiaThanhSanXuatLienTucHeSoTyLeFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
           
            Controller: TinhGiaThanhSanXuatLienTucHeSoTyLeFormController,
        }),
    });
    
    view_registry.add('tinh_gia_thanh_san_xuat_lien_tuc_he_so_ty_le_form_view', TinhGiaThanhSanXuatLienTucHeSoTyLeFormView);
    
    return TinhGiaThanhSanXuatLienTucHeSoTyLeFormView;
});
