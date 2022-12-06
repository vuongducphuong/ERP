odoo.define('sale_ex.doi_tru_chung_tu_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var DoiTruChungTuFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },

        cReload:function(ngay,loai_tien,doi_tuong,loai_chung_tu_doi_tru) {
            var self = this;
            var tham_so = {};
            var default_chi_tiet = [];
            this.rpc_action({
                model: 'sale.ex.doi.tru.chung.tu',
                method: 'lay_du_lieu_doi_tru',
                args: {
                    "NGAY" : ngay,
                    "currency_id" : loai_tien,
                    "DOI_TUONG_ID" : doi_tuong,
                    "LOAI_CHUNG_TU_DOI_TRU" : loai_chung_tu_doi_tru,
                },
                callback: function(result) {
                    if (result) {
                        self.updateUI({'SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_THANH_TOAN_IDS':result.SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_THANH_TOAN_IDS,
                                        'SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_CONG_NO_IDS' : result.SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_CONG_NO_IDS,
                        });
                    }
                }
            });
        },

        _onButtonClicked: function(event) {
            var self = this;
			event.stopPropagation();
            switch (event.data.attrs.name)
            {
                
                case "btn_lay_du_lieu":
                    var current_data = event.data.record.data;
                    var ngay;
                    var loai_tien;
                    var doi_tuong;
                    var loai_chung_tu_doi_tru;
                    if(current_data){
                        if(current_data.NGAY_DOI_TRU){
                            ngay = current_data.NGAY_DOI_TRU;
                        }
                        if(current_data.currency_id.data.id){
                            loai_tien = current_data.currency_id.data.id;
                        }
                        if(current_data.DOI_TUONG_ID){
                            doi_tuong = current_data.DOI_TUONG_ID.data.id;
                        }
                        if(current_data.LOAI_CHUNG_TU_DOI_TRU){
                            loai_chung_tu_doi_tru = current_data.LOAI_CHUNG_TU_DOI_TRU;
                        }
                        
                    }
                    self.cReload(ngay,loai_tien,doi_tuong,loai_chung_tu_doi_tru);
                    break;
                case "btn_doi_tru":
                    if(self.getFieldValue('IS_TY_GIA') == false){
                        this.rpc_action({
                            model: 'sale.ex.doi.tru.chung.tu',
                            method: 'doi_tru_chung_tu',
                            // args: {
                            //     'tai_khoan_id' : pr.tai_khoan_id,
                            // },
                            callback: function(result) {
                                var ngay;
                                var loai_tien;
                                var doi_tuong;
                                var loai_chung_tu_doi_tru;
                                if(self.getFieldValue('NGAY_DOI_TRU')){
                                    ngay = self.getFieldValue('NGAY_DOI_TRU')
                                };
                                if(self.getFieldValue('currency_id')){
                                    loai_tien = self.getFieldValue('currency_id').id
                                };
                                if(self.getFieldValue('DOI_TUONG_ID')){
                                    doi_tuong = self.getFieldValue('DOI_TUONG_ID').id
                                };
                                if(self.getFieldValue('LOAI_CHUNG_TU_DOI_TRU')){
                                    loai_chung_tu_doi_tru = self.getFieldValue('LOAI_CHUNG_TU_DOI_TRU')
                                };
                                self.cReload(ngay,loai_tien,doi_tuong,loai_chung_tu_doi_tru);
                            }
                        });
                    }
                    else{
                        var chung_tu_thanh_toan = this.getFieldValue('SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_THANH_TOAN_IDS');
                        var chung_tu_cong_no = this.getFieldValue('SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_CONG_NO_IDS');
                        var arr_hach_toan = [[5]];
                        var param_tham_so = [[5]];
                        var arr_chung_tu_cong_no = [[5]];
                        var tong_tien_doi_tru_thanh_toan = 0;
                        var tong_tien_doi_tru_cong_no = 0;
                        var tong_tien_doi_tru_quy_doi = 0;
                        var tong_tien_cong_no_quy_doi = 0;
                        var chenh_lech_tien_quy_doi = 0;
                        var arr_chung_tu = [[5]];
                        var dich_du_lieu_master
                        if(chung_tu_thanh_toan.length > 0 && chung_tu_cong_no.length > 0){
                            var doi_tuong = this.getFieldValue('DOI_TUONG_ID');
                            // Lấy dữ liệu cho master
                            var tk_xu_ly_do = this.getFieldValue('TAI_KHOAN_PHAI_THU_ID');
                            dich_du_lieu_master = {
                                'LY_DO' : 'Xử lý chênh lệch tỷ giá khi thực hiện đối trừ chứng từ',
                                'TK_XU_LY_LO_ID' : [tk_xu_ly_do.id,tk_xu_ly_do.display_name],
                                'NGAY_DOI_TRU' : this.getFieldValue('NGAY_DOI_TRU'),
                                'currency_id' : this.getFieldValue('currency_id'),
                                'LOAI_CHUNG_TU' : 4013,
                            }
                            param_tham_so.push({'dich_du_lieu_master' : dich_du_lieu_master});
                            var tk_phai_thu;
                            var tk_phai_tra;
                            var currency_id;
                            var doi_tuong_id;
                            var chenh_lech_bu_tru_cong_no = 0;
                            if(this.getFieldValue('currency_id')){
                                currency_id = this.getFieldValue('currency_id').id;
                            }
                            if(this.getFieldValue('DOI_TUONG_ID')){
                                doi_tuong_id = this.getFieldValue('DOI_TUONG_ID');
                            }
                            if(this.getFieldValue('TAI_KHOAN_PHAI_THU_ID')){
                                tk_phai_thu = this.getFieldValue('TAI_KHOAN_PHAI_THU_ID').id;
                            }
                            if(this.getFieldValue('TK_PHAI_TRA_ID')){
                                tk_phai_tra = this.getFieldValue('TK_PHAI_TRA_ID').id;
                            }
                            if(this.getFieldValue('CHENH_LECH_BU_TRU_QUY_DOI')){
                                chenh_lech_bu_tru_cong_no = this.getFieldValue('CHENH_LECH_BU_TRU_QUY_DOI');
                            }
                            
                            // Tính tổng sổ tiền thanh toán
                            var so_dong_tich_chon_thanh_toan = 0;
                            var so_dong_tich_chon_cong_no = 0;
                            for (var i in chung_tu_thanh_toan){
                                if(chung_tu_thanh_toan[i].AUTO_SELECT == true){
                                    so_dong_tich_chon_thanh_toan += 1;
                                    if(chung_tu_thanh_toan[i].SO_TIEN_DOI_TRU){
                                        tong_tien_doi_tru_thanh_toan += chung_tu_thanh_toan[i].SO_TIEN_DOI_TRU;
                                        tong_tien_doi_tru_quy_doi += chung_tu_thanh_toan[i].SO_TIEN_DOI_TRU_QUY_DOI;
                                    }
                                }
                            };
                            // Tính tổng sổ tiền công nợ
                            for (var j in chung_tu_cong_no){
                                if(chung_tu_cong_no[j].AUTO_SELECT == true){
                                    so_dong_tich_chon_cong_no += 1;
                                    if(chung_tu_cong_no[j].SO_TIEN_DOI_TRU){
                                        tong_tien_doi_tru_cong_no += chung_tu_cong_no[j].SO_TIEN_DOI_TRU;
                                        tong_tien_cong_no_quy_doi += chung_tu_cong_no[j].SO_TIEN_DOI_TRU_QUY_DOI;
                                    }
                                }
                            }
                            chenh_lech_tien_quy_doi = Math.abs(tong_tien_doi_tru_quy_doi - tong_tien_cong_no_quy_doi);
                            if(so_dong_tich_chon_thanh_toan == 0 || so_dong_tich_chon_cong_no == 0){
                                Dialog.show_message('Thông báo', 'Bạn phải chọn các chứng từ để thực hiện đối trừ', 'ALERT')
                                .then(function(result) {
                                    return;
                                });

                                return;
                            }
                            if(tong_tien_doi_tru_thanh_toan != tong_tien_doi_tru_cong_no){
                                Dialog.show_message('Thông báo', 'Tổng số tiền bù trừ của <Chứng từ phải thu> phải bằng tổng số tiền bù trừ của <Chứng từ phải trả>', 'ALERT')
                                .then(function(result) {
                                    return;
                                });

                                return;
                            }
                            
                            var so_con_no_cho_debt = tong_tien_doi_tru_thanh_toan;
                            var so_con_no_cho_debt_quy_doi = tong_tien_doi_tru_quy_doi;
                            for (var i in chung_tu_thanh_toan){
                                var chi_tiet_thanh_toan = chung_tu_thanh_toan[i];
                                if(chi_tiet_thanh_toan.AUTO_SELECT == true){

                                    for (var j in chung_tu_cong_no){
                                        var chi_tiet_cong_no = chung_tu_cong_no[j];
                                        var so_tien_doi_tru;
                                        var so_tien_doi_tru_quy_doi;
                                        if(chi_tiet_cong_no.AUTO_SELECT == true){
                                            if(chi_tiet_thanh_toan.SO_TIEN_DOI_TRU > 0 && chi_tiet_cong_no.SO_TIEN_DOI_TRU > 0){
                                                if(chi_tiet_thanh_toan.SO_TIEN_DOI_TRU > chi_tiet_cong_no.SO_TIEN_DOI_TRU){
                                                    so_tien_doi_tru = chi_tiet_cong_no.SO_TIEN_DOI_TRU;
                                                    // so_tien_doi_tru_quy_doi = chi_tiet_cong_no.SO_TIEN_DOI_TRU_QUY_DOI;
                                                }
                                                else if(chi_tiet_thanh_toan.SO_TIEN_DOI_TRU == chi_tiet_cong_no.SO_TIEN_DOI_TRU){
                                                    so_tien_doi_tru = chi_tiet_cong_no.SO_TIEN_DOI_TRU;                                                
                                                    // so_tien_doi_tru_quy_doi = chi_tiet_cong_no.SO_TIEN_DOI_TRU_QUY_DOI;    
                                                }
                                                else{
                                                    so_tien_doi_tru = chi_tiet_thanh_toan.SO_TIEN_DOI_TRU;
                                                    // so_tien_doi_tru_quy_doi = chi_tiet_thanh_toan.SO_TIEN_DOI_TRU_QUY_DOI;
                                                }
                                                chi_tiet_thanh_toan.SO_TIEN_DOI_TRU = chi_tiet_thanh_toan.SO_TIEN_DOI_TRU - so_tien_doi_tru;
                                                chi_tiet_cong_no.SO_TIEN_DOI_TRU = chi_tiet_cong_no.SO_TIEN_DOI_TRU - so_tien_doi_tru;
                                                // chi_tiet_thanh_toan.SO_TIEN_DOI_TRU_QUY_DOI = chi_tiet_thanh_toan.SO_TIEN_DOI_TRU_QUY_DOI - so_tien_doi_tru_quy_doi;
                                                // chi_tiet_cong_no.SO_TIEN_DOI_TRU_QUY_DOI = chi_tiet_cong_no.SO_TIEN_DOI_TRU_QUY_DOI - so_tien_doi_tru_quy_doi;

                                                // chế dữ liệu hiển thị trên form
                                                var dict_bu_tru_cong_no_phai_thu = {
                                                    'NGAY_CHUNG_TU_THANH_TOAN' : chi_tiet_thanh_toan.NGAY_CHUNG_TU,
                                                    'SO_CHUNG_TU_THANH_TOAN' : chi_tiet_thanh_toan.SO_CHUNG_TU,
                                                    'SO_CHUA_THANH_TOAN': chi_tiet_thanh_toan.SO_TIEN,
                                                    'SO_CHUA_THANH_TOAN_QUY_DOI': chi_tiet_thanh_toan.SO_TIEN_QUY_DOI,
                                                    'SO_TIEN_THANH_TOAN' : chi_tiet_thanh_toan.SO_CHUA_THU,
                                                    'SO_TIEN_THANH_TOAN_QUY_DOI' : chi_tiet_thanh_toan.SO_TIEN_DOI_TRU_QUY_DOI,
                                                    'SO_THANH_TOAN_LAN_NAY' : so_tien_doi_tru,
                                                    'SO_THANH_TOAN_LAN_NAY_QUY_DOI' : chi_tiet_thanh_toan.SO_TIEN_DOI_TRU_QUY_DOI,
//                                                     'SO_THANH_TOAN_LAN_NAY_QUY_DOI' : chi_tiet_thanh_toan.SO_TIEN_DOI_TRU_QUY_DOI,
                                                    'ID_CHUNG_TU_THANH_TOAN' : chi_tiet_thanh_toan.ID_CHUNG_TU_THANH_TOAN,
                                                    'MODEL_CHUNG_TU_THANH_TOAN' : chi_tiet_thanh_toan.MODEL_CHUNG_TU_THANH_TOAN,
                                                    'TEN_LOAI_CHUNG_TU_THANH_TOAN' : chi_tiet_thanh_toan.TEN_LOAI_CHUNG_TU,
                                                    'SO_HOA_DON_THANH_TOAN' : chi_tiet_thanh_toan.SO_HOA_DON,
            
                                                    'NGAY_CHUNG_TU_CONG_NO' : chi_tiet_cong_no.NGAY_CHUNG_TU,
                                                    'SO_CHUNG_TU_CONG_NO' : chi_tiet_cong_no.SO_CHUNG_TU,
                                                    'SO_HOA_DON_CONG_NO' : chi_tiet_cong_no.SO_HOA_DON,
                                                    'SO_TIEN_CON_NO' : chi_tiet_cong_no.SO_TIEN,
                                                    'SO_TIEN_CON_NO_QUY_DOI' : chi_tiet_cong_no.SO_TIEN_QUY_DOI,
                                                    'SO_TIEN_CONG_NO' : chi_tiet_cong_no.SO_CON_NO,
                                                    'SO_TIEN_CONG_NO_QUY_DOI' : chi_tiet_cong_no.SO_CON_NO_QUY_DOI,
                                                    'SO_CONG_NO_THANH_TOAN_LAN_NAY' : so_tien_doi_tru,
                                                    'SO_CONG_NO_THANH_TOAN_LAN_NAY_QUY_DOI' : chi_tiet_cong_no.SO_TIEN_DOI_TRU_QUY_DOI,
                                                    'TEN_LOAI_CHUNG_TU_CONG_NO' : chi_tiet_cong_no.TEN_LOAI_CHUNG_TU,
                                                    'ID_CHUNG_TU_CONG_NO' : chi_tiet_cong_no.ID_CHUNG_TU_CONG_NO,
                                                    'MODEL_CHUNG_TU_CONG_NO' : chi_tiet_cong_no.MODEL_CHUNG_TU_CONG_NO,
                                                    'LOAI_DOI_TRU' : '2',
                                                    'HIEN_TREN_BU_TRU' : false,
                                                    'TAI_KHOAN_ID' : tk_phai_thu,
                                                    'currency_id' : currency_id,
                                                    'CTCN_DA_GHI_SO' : false,
                                                    'CTTT_DA_GHI_SO' : false,
                                                    'CHENH_LECH_TY_GIA' : chi_tiet_thanh_toan.SO_TIEN_DOI_TRU_QUY_DOI - chi_tiet_cong_no.SO_TIEN_DOI_TRU_QUY_DOI,
                                                    'DOI_TUONG_ID' : doi_tuong_id.id,
                                                }
                                                arr_chung_tu_cong_no.push([0, 0, dict_bu_tru_cong_no_phai_thu]);
                                            }
                                        }
                                    }
                                }
                            }
                            arr_hach_toan.push([0, 0, {
                                'DIEN_GIAI' : 'Bù trừ công nợ phải thu, phải trả',
                                'SO_TIEN_QUY_DOI' : chenh_lech_tien_quy_doi,
                                'SO_TIEN' : 0,
                                'TK_NO_ID' : [this.getFieldValue('TAI_KHOAN_PHAI_THU_ID').id,this.getFieldValue('TAI_KHOAN_PHAI_THU_ID').display_name],
                                'TK_CO_ID': [this.getFieldValue('TK_XU_LY_CL_LAI_ID').id,this.getFieldValue('TK_XU_LY_CL_LAI_ID').display_name],
                                'DOI_TUONG_NO_ID' : [doi_tuong.id,doi_tuong.display_name],
                                'TEN_DOI_TUONG_NO' : doi_tuong.display_name,
                            
                            }])
                            param_tham_so.push({'arr_hach_toan' : arr_hach_toan});
                            param_tham_so.push({'arr_chung_tu_cong_no' : arr_chung_tu_cong_no});
                            param_tham_so.push({'arr_chung_tu' : arr_chung_tu});
                            
                        }

                        
                        var options = {
                            params : {param_doi_tru_chung_tu: param_tham_so},
                            res_model: 'account.ex.chung.tu.nghiep.vu.khac',
                            ref_view: 'tong_hop.view_account_ex_chung_tu_nghiep_vu_khac_form',
                        }
                        return this.openFormView(options);
                    }
                    break;

                default: 
                   this._super.apply(this, arguments);
            }
            
        },


        onRowChanged: function(field, columnName, newValue, recordValue, record) {
            var localData = this.getLocalData();
            var self = this;
            if ('AUTO_SELECT' == columnName) {
                var tong_tien_thanh_toan = 0;
                var tong_tien_cong_no = 0;
                var ty_gia_de_nhan = 0;
                var chung_tu_thanh_toan = this.getFieldValue('SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_THANH_TOAN_IDS');
                var chung_no_cong_no = this.getFieldValue('SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_CONG_NO_IDS');
                var chung_no_cong_no_moi = [[5]];
                var chung_tu_thanh_toan_moi = [[5]];
                var i = 0;
                for(i in chung_no_cong_no){
                    if(chung_no_cong_no[i].AUTO_SELECT == true){
                        tong_tien_thanh_toan += chung_no_cong_no[i].SO_CON_NO
                    }
                }
                i = 0;
				for ( i in chung_tu_thanh_toan){
                    if( chung_tu_thanh_toan[i].AUTO_SELECT == true){
                        tong_tien_cong_no += chung_tu_thanh_toan[i].SO_CHUA_DOI_TRU
                    }
                }

                i = 0;
				// trường hợp tích chọn cả hai		
				if( tong_tien_cong_no > 0 && tong_tien_thanh_toan > 0){
                    if (tong_tien_thanh_toan > tong_tien_cong_no){
                        for( i in chung_tu_thanh_toan){
                            var newval = chung_tu_thanh_toan[i];
                            if (chung_tu_thanh_toan[i].AUTO_SELECT == true){
                                if(chung_tu_thanh_toan[i].TY_GIA_DANH_GIA_LAI > 0){
                                    ty_gia_de_nhan = chung_tu_thanh_toan[i].TY_GIA_DANH_GIA_LAI
                                }else{
                                    ty_gia_de_nhan = chung_tu_thanh_toan[i].TY_GIA
                                }
                                _.extend(newval,{'SO_TIEN_DOI_TRU': chung_tu_thanh_toan[i].SO_CHUA_DOI_TRU,
                                                'SO_TIEN_DOI_TRU_QUY_DOI': chung_tu_thanh_toan[i].SO_CHUA_DOI_TRU*ty_gia_de_nhan
                                            });
                            }
                            if (chung_tu_thanh_toan[i].AUTO_SELECT == false){
                                _.extend(newval,{'SO_TIEN_DOI_TRU': 0
                                    // ,'SO_TIEN_DOI_TRU_QUY_DOI': 0
                                });
                            }
                            chung_tu_thanh_toan_moi.push([0, 0, newval]);
                        }

                        i = 0;
                        for( i in chung_no_cong_no){
                            var newval = chung_no_cong_no[i];            
                            if (chung_no_cong_no[i].AUTO_SELECT == true){
                                if(chung_no_cong_no[i].TY_GIA_DANH_GIA_LAI > 0){
                                    ty_gia_de_nhan = chung_no_cong_no[i].TY_GIA_DANH_GIA_LAI
                                }else{
                                    ty_gia_de_nhan = chung_no_cong_no[i].TY_GIA
                                };
                                if (tong_tien_cong_no == 0){
                                    chung_no_cong_no[i].SO_TIEN_DOI_TRU = 0
                                }else if( chung_no_cong_no[i].SO_CON_NO < tong_tien_cong_no){
                                    _.extend(newval,{'SO_TIEN_DOI_TRU': chung_no_cong_no[i].SO_CON_NO,
                                                     'SO_TIEN_DOI_TRU_QUY_DOI': chung_no_cong_no[i].SO_CON_NO*ty_gia_de_nhan
                                                    });
									tong_tien_cong_no = tong_tien_cong_no - chung_no_cong_no[i].SO_TIEN_DOI_TRU
                                }else if( chung_no_cong_no[i].SO_CON_NO > tong_tien_cong_no){
                                    _.extend(newval,{'SO_TIEN_DOI_TRU': tong_tien_cong_no
                                    ,'SO_TIEN_DOI_TRU_QUY_DOI': tong_tien_cong_no*ty_gia_de_nhan
                                    });
									tong_tien_cong_no = 0
                                }
                            }
                            chung_no_cong_no_moi.push([0, 0, newval]);
                        }
                        i = 0;
                    }else if (tong_tien_thanh_toan < tong_tien_cong_no){
                        for (i in chung_no_cong_no){
                            var newval = chung_no_cong_no[i];
                            if(chung_no_cong_no[i].TY_GIA_DANH_GIA_LAI > 0){
                                ty_gia_de_nhan = chung_no_cong_no[i].TY_GIA_DANH_GIA_LAI
                            }else{
                                ty_gia_de_nhan = chung_no_cong_no[i].TY_GIA
                            };
                            if (chung_no_cong_no[i].AUTO_SELECT == true){
                                _.extend(newval,{'SO_TIEN_DOI_TRU': chung_no_cong_no[i].SO_CON_NO,
                                                'SO_TIEN_DOI_TRU_QUY_DOI': chung_no_cong_no[i].SO_CON_NO*ty_gia_de_nhan
                                            });
                            }
                            if (chung_no_cong_no[i].AUTO_SELECT == false){
                                _.extend(newval,{'SO_TIEN_DOI_TRU': 0
                                    ,'SO_TIEN_DOI_TRU_QUY_DOI': 0
                                });
                            }
                            chung_no_cong_no_moi.push([0, 0, newval]);
                        }
                         i = 0;
                        for (i in chung_tu_thanh_toan){
                            var newval = chung_tu_thanh_toan[i];
                            if(chung_tu_thanh_toan[i].TY_GIA_DANH_GIA_LAI > 0){
                                ty_gia_de_nhan = chung_tu_thanh_toan[i].TY_GIA_DANH_GIA_LAI
                            }else{
                                ty_gia_de_nhan = chung_tu_thanh_toan[i].TY_GIA
                            };
                            if (chung_tu_thanh_toan[i].AUTO_SELECT == true){
                                if (tong_tien_thanh_toan == 0){
                                    chung_tu_thanh_toan[i].SO_TIEN_DOI_TRU = 0
                                }else if (tong_tien_thanh_toan > chung_tu_thanh_toan[i].SO_CHUA_DOI_TRU){
                                    //so_tien_bu_tru_phai_thu = chung_tu_thanh_toan[i].SO_CHUA_DOI_TRU
                                    _.extend(newval,{'SO_TIEN_DOI_TRU': chung_tu_thanh_toan[i].SO_CHUA_DOI_TRU,
                                                    // 'SO_TIEN_DOI_TRU_QUY_DOI': chung_tu_thanh_toan[i].SO_CHUA_DOI_TRU*ty_gia_de_nhan
                                                });
                                    tong_tien_thanh_toan = tong_tien_thanh_toan - chung_tu_thanh_toan[i].SO_TIEN_DOI_TRU
                                }else if (tong_tien_thanh_toan  < chung_tu_thanh_toan[i].SO_CHUA_DOI_TRU){
                                    //so_tien_bu_tru_phai_thu = tong_tien_thanh_toan
                                    _.extend(newval,{'SO_TIEN_DOI_TRU': tong_tien_thanh_toan
                                        ,'SO_TIEN_DOI_TRU_QUY_DOI': tong_tien_thanh_toan*ty_gia_de_nhan
                                        });
                                    tong_tien_thanh_toan = 0
                                }
                            }
                            chung_tu_thanh_toan_moi.push([0, 0, newval]);
                        }
                        i = 0;
                    }
                }
                else if(tong_tien_cong_no > 0){
                    i = 0;
                    for(i in chung_tu_thanh_toan){
                        var newval = chung_tu_thanh_toan[i];
                        if(chung_tu_thanh_toan[i].TY_GIA_DANH_GIA_LAI > 0){
                            ty_gia_de_nhan = chung_tu_thanh_toan[i].TY_GIA_DANH_GIA_LAI
                        }else{
                            ty_gia_de_nhan = chung_tu_thanh_toan[i].TY_GIA
                        };
                        if(chung_tu_thanh_toan[i].AUTO_SELECT == true && recordValue.ID_GOC == chung_tu_thanh_toan[i].ID_GOC && recordValue.MODEL_GOC == chung_tu_thanh_toan[i].MODEL_GOC){                            
                            _.extend(newval,{'SO_TIEN_DOI_TRU': chung_tu_thanh_toan[i].SO_CHUA_DOI_TRU,
                                             'SO_TIEN_DOI_TRU_QUY_DOI': chung_tu_thanh_toan[i].SO_CHUA_DOI_TRU*ty_gia_de_nhan,
                                             'AUTO_SELECT' : true,
                                            });
                        }else if(chung_tu_thanh_toan[i].AUTO_SELECT == false && recordValue.ID_GOC == chung_tu_thanh_toan[i].ID_GOC && recordValue.MODEL_GOC == chung_tu_thanh_toan[i].MODEL_GOC){
                             _.extend(newval,{'SO_TIEN_DOI_TRU': 0
                                ,'SO_TIEN_DOI_TRU_QUY_DOI': 0
                            });
                        }
                        chung_tu_thanh_toan_moi.push([0, 0, newval]);
                    };

                    i = 0;
                    for(i in chung_no_cong_no){
                        var newval = chung_no_cong_no[i];
                        chung_no_cong_no_moi.push([0, 0, newval]);
                    }
                }
                else if(tong_tien_thanh_toan > 0){
                                        i = 0;
                    for(i in chung_no_cong_no){
                        var newval = chung_no_cong_no[i];
                        if(chung_no_cong_no[i].TY_GIA_DANH_GIA_LAI > 0){
                            ty_gia_de_nhan = chung_no_cong_no[i].TY_GIA_DANH_GIA_LAI
                        }else{
                            ty_gia_de_nhan = chung_no_cong_no[i].TY_GIA
                        };
                        if(chung_no_cong_no[i].AUTO_SELECT == true && recordValue.ID_GOC == chung_no_cong_no[i].ID_GOC && recordValue.MODEL_GOC == chung_no_cong_no[i].MODEL_GOC){                            
                            _.extend(newval,{'SO_TIEN_DOI_TRU': chung_no_cong_no[i].SO_CON_NO,
                                             'SO_TIEN_DOI_TRU_QUY_DOI': chung_no_cong_no[i].SO_CON_NO*ty_gia_de_nhan,
                                             'AUTO_SELECT' : true,
                                            });
                        }
                        else if(chung_no_cong_no[i].AUTO_SELECT == false && recordValue.ID_GOC == chung_no_cong_no[i].ID_GOC && recordValue.MODEL_GOC == chung_no_cong_no[i].MODEL_GOC){
                             _.extend(newval,{'SO_TIEN_DOI_TRU': 0
                                ,'SO_TIEN_DOI_TRU_QUY_DOI': 0
                            });
                        }
                        chung_no_cong_no_moi.push([0, 0, newval]);
                    };
                    i = 0;
                    for(i in chung_tu_thanh_toan){
                        var newval = chung_tu_thanh_toan[i];
                        chung_tu_thanh_toan_moi.push([0, 0, newval]);
                    }
                }
                else{
                    i = 0;
                    for(i in chung_tu_thanh_toan){
                        var newval = chung_tu_thanh_toan[i];
                        if(recordValue.ID_GOC == chung_tu_thanh_toan[i].ID_GOC && recordValue.MODEL_GOC == chung_tu_thanh_toan[i].MODEL_GOC){                            
                            _.extend(newval,{'SO_TIEN_DOI_TRU': 0
                                ,'SO_TIEN_DOI_TRU_QUY_DOI': 0
                            });
                        }
                        chung_tu_thanh_toan_moi.push([0, 0, newval]);
                    };

                    i = 0;
                    for(i in chung_no_cong_no){
                        var newval = chung_no_cong_no[i];
                        if(recordValue.ID_GOC == chung_no_cong_no[i].ID_GOC && recordValue.MODEL_GOC == chung_no_cong_no[i].MODEL_GOC){                            
                            _.extend(newval,{'SO_TIEN_DOI_TRU': 0,'SO_TIEN_DOI_TRU': 0});
                        }
                        chung_no_cong_no_moi.push([0, 0, newval]);
                    }
                }

                this.updateUI({'SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_THANH_TOAN_IDS': chung_tu_thanh_toan_moi});
                this.updateUI({'SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_CONG_NO_IDS': chung_no_cong_no_moi});
            }
            return true;
        },

    });
    
    var DoiTruChungTuFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: DoiTruChungTuFormController,
        }),
    });
    
    view_registry.add('doi_tru_chung_tu_form_view', DoiTruChungTuFormView);
    
    return DoiTruChungTuFormView;
});
