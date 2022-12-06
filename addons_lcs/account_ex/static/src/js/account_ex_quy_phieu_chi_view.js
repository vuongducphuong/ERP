odoo.define('account_ex.account_ex_quy_phieu_chi_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var PhieuChiController = FormController.extend({
        getPrintBlackList:function () {
            var blackList = {};
            if (this.getFieldValue('LOAI_PHIEU')=='PHIEU_CHI') {
                blackList['01-TT Phiếu thu'] = true;
                blackList['Giấy báo nợ'] = true;
                blackList['Giấy báo có'] = true;
                blackList['Ủy nhiệm chi (BIDV)'] = true;
                blackList['01-TT Phiếu thu(Mẫu đầy đủ)'] = true;
                blackList['01-TT Phiếu thu(Mẫu A5)'] = true;
                blackList['01-TT Phiếu thu(Mẫu 2 liên)'] = true;
                blackList['Uỷ nhiệm chi (agribank)'] = true;
                blackList['Uỷ nhiệm chi (SHB)'] = true;
                blackList['Uỷ nhiệm chi Viettinbank'] = true;
                blackList['Uỷ nhiệm chi (MB)'] = true;
                blackList['Uỷ nhiệm chi Techcombank'] = true;
                blackList['Uỷ nhiệm chi (Vietcombank)'] = true;
                blackList['Uỷ nhiệm chi (PVC)'] = true;
            }
            return blackList;
        },
        onViewLoaded: function(e, defer) {
			var def = defer;
            var self = this;
            if(this.params){
                if(this.params.param_bu_tru_cong_no){
                    var du_lieu = this.params.param_bu_tru_cong_no;
                    self.updateUI({'SALE_EX_DOI_TRU_CHI_TIET_IDS': du_lieu[3].arr_chung_tu_cong_no});
                    self.updateUI({'ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS': du_lieu[2].arr_hach_toan});
                    self.changeFieldValue('LOAI_CHUNG_TU_QTTU_NVK', 'BU_TRU_CN');
                    self.changeFieldValue('DOI_TUONG_ID', du_lieu[1].dich_du_lieu_master.DOI_TUONG_ID);
                    self.changeFieldValue('TEN_DOI_TUONG', du_lieu[1].dich_du_lieu_master.TEN_DOI_TUONG);
                    self.changeFieldValue('DIEN_GIAI', du_lieu[1].dich_du_lieu_master.LY_DO);
                    self.changeFieldValue('TK_XU_LY_LAI_ID', du_lieu[1].dich_du_lieu_master.TAI_KHOAN_PHAI_THU);
                    self.changeFieldValue('TK_XU_LY_LO_ID',du_lieu[1].dich_du_lieu_master.TAI_KHOAN_PHAI_TRA);
//                     self.changeFieldValue('NGAY_BU_TRU', du_lieu[1].dich_du_lieu_master.NGAY_BU_TRU);
                    self.changeFieldValue('currency_id', du_lieu[1].dich_du_lieu_master.currency_id);
                    // self.changeFieldValue('NGAY_HACH_TOAN', du_lieu[1].dich_du_lieu_master.NGAY_BU_TRU._i);
                    // self.changeFieldValue('NGAY_CHUNG_TU', du_lieu[1].dich_du_lieu_master.NGAY_BU_TRU._i);
                     var fieldWidget = this.getFieldWidget('SALE_EX_DOI_TRU_CHI_TIET_IDS');
                     fieldWidget.do_filter(['HIEN_TREN_BU_TRU', '=', true]);
                }
                else{
                    if(this.params.params && this.params.params.LOAI_CHUNG_TU_DANH_GIA_LAI){
                        var gia_tri_params = this.params.params;
                        self.changeFieldValue('LOAI_CHUNG_TU_QTTU_NVK', gia_tri_params.LOAI_CHUNG_TU_DANH_GIA_LAI);
                        self.changeFieldValue('TK_XU_LY_LAI_ID', gia_tri_params.TK_XU_LY_LAI_CHENH_LECH_TY_GIA_ID);
                        self.changeFieldValue('TK_XU_LY_LO_ID', gia_tri_params.TK_XU_LY_LO_CHENH_LECH_TY_GIA_ID);
                        self.updateUI({'TONG_HOP_CHUNG_TU_NGHIEP_VU_KHAC_SO_DU_NGOAI_TE_IDS': gia_tri_params.TONG_HOP_CHUNG_TU_NGHIEP_VU_KHAC_SO_DU_NGOAI_TE_IDS});
                        self.updateUI({'TONG_HOP_CHUNG_TU_NGHIEP_VU_KHAC_CONG_NO_THANH_TOAN_IDS': gia_tri_params.TONG_HOP_CHUNG_TU_NGHIEP_VU_KHAC_CONG_NO_THANH_TOAN_IDS});
                        self.updateUI({'ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS': gia_tri_params.ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS});
                    }
                    if(this.params.params && this.params.params.LOAI_TO_KHAI){
                        self.changeFieldValue('LOAI_TO_KHAI', this.params.params.LOAI_TO_KHAI);
                    }
                    if(this.params.params && this.params.params.QUY){
                        self.changeFieldValue('KY_TINH_THUE_QUY', this.params.params.QUY);
                    }
                    if(this.params.params && this.params.params.THANG){
                        self.changeFieldValue('KY_TINH_THUE_THANG', this.params.params.THANG);
                    }
                    if(this.params.params && this.params.params.NAM){
                        self.changeFieldValue('NAM', this.params.params.NAM);
                    }
                }
            }
            
            def.resolve();
        },
        onRowChanged: function(field, columnName, newValue, recordValue, record) {
            var self = this;
            if (field == 'ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS'){
                if(columnName=='DOI_TUONG_ID'){
                    var hach_toan_chi_tiets = this.getFieldValue('ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS');
                    var thue_chi_tiets= this.getFieldValue('ACCOUNT_EX_PHIEU_THU_CHI_THUE_IDS');
                    if(hach_toan_chi_tiets.length > 0){
                        
                       if(hach_toan_chi_tiets[0].res_id==record.id){
                           var doi_tuong_id = hach_toan_chi_tiets[0].DOI_TUONG_ID.id;
                           var ma_doi_tuong = hach_toan_chi_tiets[0].DOI_TUONG_ID.display_name;
                           if (thue_chi_tiets.length > 0){
                               for(var i = 0 ; i < thue_chi_tiets.length ; i++){
                                  self.updateUI({'ACCOUNT_EX_PHIEU_THU_CHI_THUE_IDS': [[1,thue_chi_tiets[i].res_id,{'DOI_TUONG_ID':[doi_tuong_id,ma_doi_tuong]}]]});


                               }

                           }
    

                        }
                        

                    }


                    var a = 0;
                }

            }
            return true;
        },


    });
    var PhieuChiView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: PhieuChiController,
        }),
    });
    
    view_registry.add('account_ex_quy_phieu_chi_form_view', PhieuChiView);
    
    return PhieuChiView;
});

odoo.define('account_ex.account_ex_quy_phieu_chi_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');

    var PhieuChiController = ListController.extend({
        getPrintBlackList:function () {
            var blackList = {};
            var selectedRecords = this.getSelectedRecords();
            for (var i=0; i<selectedRecords.length; i++) {
                var record = selectedRecords[i].data;
                if (record.LOAI_PHIEU == 'PHIEU_CHI') {
                    blackList['01-TT Phiếu thu'] = true;
                    blackList['Giấy báo nợ'] = true;
                    blackList['Giấy báo có'] = true;
                    blackList['Ủy nhiệm chi (BIDV)'] = true;
                    blackList['01-TT Phiếu thu(Mẫu đầy đủ)'] = true;
                    blackList['01-TT Phiếu thu(Mẫu A5)'] = true;
                    blackList['01-TT Phiếu thu(Mẫu 2 liên)'] = true;
                    blackList['Uỷ nhiệm chi (agribank)'] = true;
                    blackList['Uỷ nhiệm chi (SHB)'] = true;
                    blackList['Uỷ nhiệm chi Viettinbank'] = true;
                    blackList['Uỷ nhiệm chi (MB)'] = true;
                    blackList['Uỷ nhiệm chi Techcombank'] = true;
                    blackList['Uỷ nhiệm chi (Vietcombank)'] = true;
                    blackList['Uỷ nhiệm chi (PVC)'] = true;
                }
            }
            return blackList;
        },
    });
    
    var PhieuChiView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: PhieuChiController,
        }),
    });
    
    view_registry.add('account_ex_quy_phieu_chi_list_view', PhieuChiView);
    
    return PhieuChiView;
});