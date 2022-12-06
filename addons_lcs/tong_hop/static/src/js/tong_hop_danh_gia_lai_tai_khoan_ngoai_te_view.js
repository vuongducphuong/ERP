odoo.define('tong_hop.tong_hop_danh_gia_lai_tai_khoan_ngoai_te_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormRenderer = require('web.FormRenderer');
    var BasicModel = require('web.BasicModel');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var TongHopDanhGiaLaiTaiKhoanNgoaiTeController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },

        onViewLoaded: function(e, defer) {
			var def = defer;
            var self = this;
            this.rpc_action({
                model: 'tong.hop.danh.gia.lai.tai.khoan.ngoai.te',
                method: 'load_UI',
                // args: {},
                callback: function(result) {
                    if (result) {
                        self.updateUI(result);
                    }
					if (def) {
                        def.resolve();
                    }
                }
            });
        },
        onFieldChanged: function(field){
            var self = this;
            if("DANH_GIA_NGOAI_TE_ID" == field){
                var kiem_tra_gia_tri_ngoai_te = this.getFieldValue('DANH_GIA_NGOAI_TE_ID');
                if(kiem_tra_gia_tri_ngoai_te != null){
                    var loai_tien_id = this.getFieldValue('DANH_GIA_NGOAI_TE_ID').id;
                }
                this.rpc_action({
                    model: 'tong.hop.danh.gia.lai.tai.khoan.ngoai.te',
                    method: 'load_ud',
                    args: {
                        'loai_tien_id' : loai_tien_id,
                    },
                    callback: function(result) {
                        if (result) {
                            self.updateUI(result);
                        }
                    }
                });
            }
            
        },
        onRowChanged: function(field, columnName, newValue, recordValue, record) {
            var localData = this.getLocalData();
            if (columnName == 'AUTO_SELECT') {
                var loai_tien_id = this.getFieldValue('DANH_GIA_NGOAI_TE_ID').id;
                var fieldWidget = this.getFieldWidget('TONG_HOP_DANH_GIA_LAI_TAI_KHOAN_NGOAI_TE_CONG_NO_THANH_TOAN_IDS');
                var so_du_ngoai_te = this.getFieldValue('TONG_HOP_DANH_GIA_LAI_TAI_KHOAN_NGOAI_TE_SO_DU_NGOAI_TE_IDS');
                var dieu_kien = [];
                if(so_du_ngoai_te.length > 0){
                    for(var i in so_du_ngoai_te){
                        if(so_du_ngoai_te[i].AUTO_SELECT == true){
                            var doi_tuong_id_str = '';
                            var tai_khoan_id_str = '';
                            if(so_du_ngoai_te[i].DOI_TUONG_ID){
                                doi_tuong_id_str = so_du_ngoai_te[i].DOI_TUONG_ID.id.toString();
                            }
                            if(so_du_ngoai_te[i].TAI_KHOAN_ID){
                                tai_khoan_id_str = so_du_ngoai_te[i].TAI_KHOAN_ID.id.toString();
                            }
                            var dieu_kien_so_du_ngoai_te = tai_khoan_id_str + ',' + doi_tuong_id_str;
                            dieu_kien.push([ "ID_TK_VA_ID_DOI_TUONG", "=", dieu_kien_so_du_ngoai_te ]);                            
                            dieu_kien.push("or");
                        }
                    }
                    if(dieu_kien){
                        dieu_kien.pop("or");
                    }
                }
                fieldWidget.do_filter(dieu_kien);
                // this.rpc_action({
                //     model: 'tong.hop.danh.gia.lai.tai.khoan.ngoai.te',
                //     method: 'load_ud',
                //     args: {
                //         'loai_tien_id' : loai_tien_id,
                //     },
                //     callback: function(result) {
                //         if (result) {
                //             self.updateUI(result);
                //         }
                //     }
                // });
            }
            return true;
        },

        _onButtonClicked: function(event) {
            var self = this;
			event.stopPropagation();
            switch (event.data.attrs.id)
            {
                case "btn_thuc_hien":
                    var data =this.getLocalData();
                    var default_chi_tiet_so_du_ngoai_te = [];
                    var default_chi_tiet_cong_no_va_thanh_toan = [];
                    var default_chi_tiet_hach_toan_danh_gia_lai_tk_ngoai_te = [];
                    var data_so_du_ngoai_te_chitiet = data.TONG_HOP_DANH_GIA_LAI_TAI_KHOAN_NGOAI_TE_SO_DU_NGOAI_TE_IDS;

                    for (var i=0; i< data_so_du_ngoai_te_chitiet.length; i++) {
                        var chi_tiet = data_so_du_ngoai_te_chitiet[i];
                        if(chi_tiet.AUTO_SELECT == true){
                            default_chi_tiet_so_du_ngoai_te.push([0, 0, {
                                'TAI_KHOAN_ID': [chi_tiet.TAI_KHOAN_ID.id,chi_tiet.TAI_KHOAN_ID.display_name],
                                'TK_NGAN_HANG_ID':  [chi_tiet.TK_NGAN_HANG_ID.id,chi_tiet.TK_NGAN_HANG_ID.display_name],
                                'TEN_NGAN_HANG': chi_tiet.TEN_NGAN_HANG,
                                'DOI_TUONG_ID': [chi_tiet.DOI_TUONG_ID.id,chi_tiet.DOI_TUONG_ID.display_name],
                                'TY_GIA': chi_tiet.TY_GIA,
                                'SO_TIEN_DU_NO': chi_tiet.SO_TIEN_DU_NO,
                                'QUY_DOI_DU_NO': chi_tiet.QUY_DOI_DU_NO,
                                'DANH_GIA_LAI_DU_NO': chi_tiet.DANH_GIA_LAI_DU_NO,
                                'CHENH_LECH_DU_NO': chi_tiet.CHENH_LECH_DU_NO,
                                'SO_TIEN_DU_CO': chi_tiet.SO_TIEN_DU_CO,
                                'QUY_DOI_DU_CO': chi_tiet.QUY_DOI_DU_CO,
                                'DANH_GIA_LAI_DU_CO': chi_tiet.DANH_GIA_LAI_DU_CO,
                                'CHENH_LECH_DU_CO': chi_tiet.CHENH_LECH_DU_CO,
                            }])
                        }
                        
                    }

                    // Kiểm tra những dòng nào có số tiền chênh lệch dư nợ và dư có != 0 thì chuyển sang form sau

                    for (var i=0; i< data_so_du_ngoai_te_chitiet.length; i++) {
                        var sotien ;
                        var chi_tiet = data_so_du_ngoai_te_chitiet[i];
                        if(chi_tiet.CHENH_LECH_DU_NO !=0){
                            sotien = chi_tiet.CHENH_LECH_DU_NO;
                            if(sotien > 0){
                                var TK_CO = [data.TK_XU_LY_LAI_CHENH_LECH_TY_GIA_ID.id, data.TK_XU_LY_LAI_CHENH_LECH_TY_GIA_ID.display_name];
                                var TK_NO = [chi_tiet.TAI_KHOAN_ID.id,chi_tiet.TAI_KHOAN_ID.display_name]
                            }
                            else{
                                var TK_CO =[chi_tiet.TAI_KHOAN_ID.id,chi_tiet.TAI_KHOAN_ID.display_name]
                                var TK_NO = [data.TK_XU_LY_LO_CHENH_LECH_TY_GIA_ID.id, data.TK_XU_LY_LO_CHENH_LECH_TY_GIA_ID.display_name];
                            }
                            default_chi_tiet_hach_toan_danh_gia_lai_tk_ngoai_te.push([0, 0, {
                                'DIEN_GIAI': 'Lỗ do xử lý chênh lệch tỷ giá từ đánh giá lại ngoại tệ.',
                                'TK_NO_ID': TK_NO,
                                'TK_CO_ID': TK_CO,
                                'SO_TIEN_QUY_DOI':sotien ,
                                'TK_NGAN_HANG_ID':  [chi_tiet.TK_NGAN_HANG_ID.id,chi_tiet.TK_NGAN_HANG_ID.display_name],
                                'DOI_TUONG_CO_ID': [chi_tiet.DOI_TUONG_ID.id,chi_tiet.DOI_TUONG_ID.display_name],
                                'TEN_DOI_TUONG_CO': chi_tiet.DOI_TUONG_ID.id,
                             }])
                        }
                        else{
                            if(chi_tiet.CHENH_LECH_DU_CO !=0){
                                sotien = chi_tiet.CHENH_LECH_DU_CO;
                                if(sotien < 0){
                                    var TK_CO = [data.TK_XU_LY_LAI_CHENH_LECH_TY_GIA_ID.id, data.TK_XU_LY_LAI_CHENH_LECH_TY_GIA_ID.display_name];
                                    var TK_NO = [chi_tiet.TAI_KHOAN_ID.id,chi_tiet.TAI_KHOAN_ID.display_name]
                                }
                                else{
                                    var TK_CO =[chi_tiet.TAI_KHOAN_ID.id,chi_tiet.TAI_KHOAN_ID.display_name]
                                    var TK_NO = [data.TK_XU_LY_LO_CHENH_LECH_TY_GIA_ID.id, data.TK_XU_LY_LO_CHENH_LECH_TY_GIA_ID.display_name];
                                }
                                default_chi_tiet_hach_toan_danh_gia_lai_tk_ngoai_te.push([0, 0, {
                                    'DIEN_GIAI': 'Lỗ do xử lý chênh lệch tỷ giá từ đánh giá lại ngoại tệ.',
                                    'TK_NO_ID': TK_NO,
                                    'TK_CO_ID': TK_CO,
                                    'SO_TIEN_QUY_DOI':sotien,
                                    'TK_NGAN_HANG_ID':  [chi_tiet.TK_NGAN_HANG_ID.id,chi_tiet.TK_NGAN_HANG_ID.display_name],
                                    'DOI_TUONG_NO_ID': [chi_tiet.DOI_TUONG_ID.id,chi_tiet.DOI_TUONG_ID.display_name],
                                    'TEN_DOI_TUONG_NO': chi_tiet.DOI_TUONG_ID.id,
                                 }])
                            }
                        }

                    }

                    var data_chung_tu_cong_no_thanh_toan_chi_tiet = data.TONG_HOP_DANH_GIA_LAI_TAI_KHOAN_NGOAI_TE_CONG_NO_THANH_TOAN_IDS;
                    for (var i=0; i< data_chung_tu_cong_no_thanh_toan_chi_tiet.length; i++) {
                        var chi_tiet = data_chung_tu_cong_no_thanh_toan_chi_tiet[i];
                        default_chi_tiet_cong_no_va_thanh_toan.push([0, 0, {
                            'LOAI_CHUNG_TU': chi_tiet.LOAI_CHUNG_TU,
                            'NGAY_CHUNG_TU':  chi_tiet.NGAY_CHUNG_TU,
                            'SO_CHUNG_TU': chi_tiet.SO_CHUNG_TU,
                            'SO_HOA_DON': chi_tiet.SO_HOA_DON,
                            'DIEN_GIAI': chi_tiet.DIEN_GIAI,
                            'TK_CONG_NO_ID': [chi_tiet.TK_CONG_NO_ID.id,chi_tiet.TK_CONG_NO_ID.display_name],
                            'DOI_TUONG_ID': [chi_tiet.DOI_TUONG_ID.id,chi_tiet.DOI_TUONG_ID.display_name],
                            'TY_GIA_TREN_CT': chi_tiet.TY_GIA_TREN_CT,
                            'TY_GIA_DANH_GIA_LAI_GAN_NHAT': chi_tiet.TY_GIA_DANH_GIA_LAI_GAN_NHAT,
                            'SO_CHUA_DOI_TRU': chi_tiet.SO_CHUA_DOI_TRU,
                            'SO_CHUA_DOI_TRU_QUY_DOI': chi_tiet.SO_CHUA_DOI_TRU_QUY_DOI,
                            'TY_GIA_DANH_GIA_LAI': chi_tiet.TY_GIA_DANH_GIA_LAI_GAN_NHAT,
                            'DANH_GIA_LAI': chi_tiet.DANH_GIA_LAI,
                            'CHENH_LECH': chi_tiet.CHENH_LECH,
                            'ID_CHUNG_TU_GOC': chi_tiet.ID_CHUNG_TU_GOC,
                            'MODEL_CHUNG_TU_GOC': chi_tiet.MODEL_CHUNG_TU_GOC,
                
                    }])
                    }
    
                    var context = {
                    'TK_XU_LY_LAI_CHENH_LECH_TY_GIA_ID': data.TK_XU_LY_LAI_CHENH_LECH_TY_GIA_ID.id,
                    'TK_XU_LY_LO_CHENH_LECH_TY_GIA_ID': data.TK_XU_LY_LO_CHENH_LECH_TY_GIA_ID.id,
                    'LOAI_CHUNG_TU_DANH_GIA_LAI': 'XU_LY_CHENH_LECH_TY_GIA_TK_NGOAI_TE',
                    'DIEN_GIAI': 'Đánh giá lại số dư ngoại tệ cuối kỳ',
                    'TONG_HOP_CHUNG_TU_NGHIEP_VU_KHAC_SO_DU_NGOAI_TE_IDS': default_chi_tiet_so_du_ngoai_te  ,
                    'TONG_HOP_CHUNG_TU_NGHIEP_VU_KHAC_CONG_NO_THANH_TOAN_IDS': default_chi_tiet_cong_no_va_thanh_toan,
                    'ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS': default_chi_tiet_hach_toan_danh_gia_lai_tk_ngoai_te,
                    };
                    return new dialogs.FormViewDialog(this, _.extend({}, this.nodeOptions, {
                        model: this.model,
                        readonly: false,
                        res_model: 'account.ex.chung.tu.nghiep.vu.khac',
                        // shouldSaveLocally: true,
                        disable_multiple_selection: true,
                        // context : param,
                        params: context,
                        title: 'Xử lý chênh lệch tỷ giá từ đánh giá lại tài khoản ngoại tệ',
                        ref_views: [['tong_hop.view_account_ex_chung_tu_nghiep_vu_khac_form', 'form']],
                        
                    })).open();

                    //  Em Mạnh muốn đóng form ở đây 

                    break;
                
                default: 
                   this._super.apply(this, arguments);
            }
            
        },
        
    });

    var TongHopDanhGiaLaiTaiKhoanNgoaiTeRenderer = FormRenderer.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });

    var TongHopDanhGiaLaiTaiKhoanNgoaiTeModel = BasicModel.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });
    
    var TongHopDanhGiaLaiTaiKhoanNgoaiTeView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Model: TongHopDanhGiaLaiTaiKhoanNgoaiTeModel,
            Renderer: TongHopDanhGiaLaiTaiKhoanNgoaiTeRenderer,
            Controller: TongHopDanhGiaLaiTaiKhoanNgoaiTeController,
        }),
    });
    
    view_registry.add('tong_hop_danh_gia_lai_tai_khoan_ngoai_te_view', TongHopDanhGiaLaiTaiKhoanNgoaiTeView);
    
    return TongHopDanhGiaLaiTaiKhoanNgoaiTeView;
});
