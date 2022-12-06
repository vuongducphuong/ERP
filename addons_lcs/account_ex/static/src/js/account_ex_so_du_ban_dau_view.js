odoo.define('account_ex.account_ex_so_du_ban_dau_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var SoDuBanDauController = FormController.extend({

        onOpenOne2ManyRecord: function(data, record) {
            
            var self = this;
            var def = $.Deferred();
            var error = [];
            var Dialog = require('web.Dialog');
            if(record.data.LA_TK_TONG_HOP == true){
                error = 'Không được nhập số dư cho tài khoản tổng hợp.';
            }
            if (error.length) {
                self.notifyInvalidFields(error);
                def.resolve(false);
                return def; 
            } else {
                def.resolve(true);
            }
            
            var so_tai_khoan_id = record.data.SO_TAI_KHOAN_ID;
            var ct_theo_dt = record.data.CHI_TIET_THEO_DOI_TUONG;
            var ct_theo_tk = record.data.CHI_TIET_THEO_TK_NGAN_HANG;
          // gán test dữ liệu để mở form cho trường hợp số dư tài khoản 
            // var ct_theo_dt = 0;
            // var ct_theo_tk = 0;
//         // gán test dữ liệu để mở form cho trường hợp số dư tài khoản ngân hàng
//                var ct_theo_dt = null;
//                var ct_theo_tk = 1;
            // gán test dữ liệu để mở form cho trường hợp công nợ khách hàng 
//             var ct_theo_dt = 1;
//             var ct_theo_tk = null;
//             var loai_doi_tuong = "1";
            var loai_doi_tuong = record.data.LOAI_DOI_TUONG;
            var dict_param = {
                'ct_theo_dt' : ct_theo_dt,
                'ct_theo_tk' : ct_theo_tk,
                'loai_doi_tuong' : loai_doi_tuong,
                'loai_tien_so_du_tai_khoan_id' : this.getFieldValue('LOAI_TIEN_ID_SO_DU_TAI_KHOAN'),
                'loai_tien_so_du_tai_khoan_ngan_hang_id' : this.getFieldValue('LOAI_TIEN_ID_SO_DU_TK_NGAN_HANG'),
                'loai_tien_so_so_cong_no_khach_hang_id' : this.getFieldValue('LOAI_TIEN_ID_SO_CONG_NO_KHACH_HANG'),
                'loai_tien_so_so_cong_no_nha_cung_cap_id' : this.getFieldValue('LOAI_TIEN_ID_SO_CONG_NO_NHA_CUNG_CAP'),
                'loai_tien_so_so_cong_no_nhan_vien_id' : this.getFieldValue('LOAI_TIEN_ID_SO_CONG_NO_NHAN_VIEN'),
                'tai_khoan_id' : so_tai_khoan_id,
                'chi_tiet_vthh' : record.data.CHI_TIET_VTHH,
                'kho_id' : record.data.KHO_ID,
            }

            if(ct_theo_dt == 0 && ct_theo_tk == 0){
                new dialogs.FormViewDialog(this, {
                    tham_so : dict_param,
                    readonly: false,
                    res_model: 'account.ex.so.du.tai.khoan',
//                     size :'large',
                    ref_views: [['account_ex.view_account_ex_so_du_tai_khoan_form', 'form']],
                    title: ("Nhập số dư tài khoản"),
                    disable_multiple_selection: true,
                    save_raw_changes: true,
                    on_after_saved: function (record, changed) {
                        if (changed) {
                            self.cReload();
                        }
                    },
                }).open();
            }

            if(ct_theo_tk == 1){
                new dialogs.FormViewDialog(this, {
                    tham_so : dict_param,
                    readonly: false,
                    res_model: 'account.ex.so.du.tai.khoan',
                    // size :'large',
                    ref_views: [['account_ex.view_account_ex_so_du_tai_ngan_hang_khoan_form', 'form']],
                    title: ("Nhập số dư tài khoản ngân hàng"),
                    disable_multiple_selection: true,
                    save_raw_changes: true,
                    on_after_saved: function (record, changed) {
                        if (changed) {
                            self.cReload();
                        }
                    },
                }).open();
            }

            if(ct_theo_dt == 1 && loai_doi_tuong == "0"){
                new dialogs.FormViewDialog(this, {
                    tham_so : dict_param,
                    readonly: false,
                    res_model: 'account.ex.so.du.tai.khoan',
                    // size :'large',
                    ref_views: [['account_ex.view_account_ex_cong_no_ncc_form', 'form']],
                    title: ("Nhập số dư công nợ nhà cung cấp"),
                    disable_multiple_selection: true,
                    save_raw_changes: true,
                    on_after_saved: function (record, changed) {
                        if (changed) {
                            self.cReload();
                        }
                    },
                }).open();
            }

            if(ct_theo_dt == 1 && loai_doi_tuong == "1"){
                
                new dialogs.FormViewDialog(this, {
                    tham_so : dict_param,
                    readonly: false,
                    res_model: 'account.ex.so.du.tai.khoan',
                    // size :'large',
                    ref_views: [['account_ex.view_account_ex_cong_no_khach_hang_form', 'form']],
                    title: ("Nhập số dư công nợ khách hàng"),
                    disable_multiple_selection: true,
                    save_raw_changes: true,
                    on_after_saved: function (record, changed) {
                        if (changed) {
                            self.cReload();
                        }
                    },
                }).open();
            }

            if(ct_theo_dt == 1 && loai_doi_tuong == "2"){
                new dialogs.FormViewDialog(this, {
                    tham_so : dict_param,
                    readonly: false,
                    res_model: 'account.ex.so.du.tai.khoan',
                    ref_views: [['account_ex.view_account_ex_cong_no_nhan_vien_form', 'form']],
                    title: ("Nhập số dư công nợ nhân viên"),
                    disable_multiple_selection: true,
                    save_raw_changes: true,
                    on_after_saved: function (record, changed) {
                        if (changed) {
                            self.cReload();
                        }
                    },
                }).open();
            }
            if(record.data.CHI_TIET_VTHH == 1){
                new dialogs.FormViewDialog(this, {
                    tham_so : dict_param,
                    readonly: false,
                    res_model: 'account.ex.ton.kho.vat.tu.hang.hoa.master',
                    ref_views: [['account_ex.view_account_ex_ton_kho_vat_tu_hang_hoa_master_form', 'form']],
                    title: ("Nhập tồn kho vật tư hàng hóa"),
                    disable_multiple_selection: true,
                    save_raw_changes: true,
                    on_before_saved: function(controller) {
                        var def = $.Deferred();
                        var isDef = false;
                        var error = false;
                        var ton_kho_vthhs = controller.getFieldValue('ACCOUNT_EX_TON_KHO_VAT_TU_HANG_HOA_IDS');
                        if(ton_kho_vthhs.length > 0){
                            var arr_vthh = [];
                            for(var j in ton_kho_vthhs){
                                var vthh = ton_kho_vthhs[j];
                                if(vthh.MA_HANG_ID){
                                     if(arr_vthh.includes(vthh.MA_HANG_ID.display_name)){
                                        var loi = 'Số lô, Hạn sử dụng, Hàng hóa giữ hộ của Mã hàng <' + vthh.MA_HANG_ID.display_name + '> theo đơn vị tính <' +vthh.DVT_ID.display_name+ '> đã tồn tại. Xin vui lòng kiểm tra lại.';
                                        Dialog.show_message('tieu_de', loi, 'ALERT')
                                        .then(function(result) {
                                                // Xử lý sau khi đóng popup
                                        });
                                        error = true;
                                    }
                                    else{
                                        arr_vthh.push(vthh.MA_HANG_ID.display_name)
                                    }    
                                }
                            }
                        }
                        if (error == true) {
							// self.notifyInvalidFields(error);
							def.resolve(false);
						} else {
							def.resolve(true);
						}
						return def;                          
                    },
                    on_after_saved: function (record, changed) {
                        if (changed) {
                            self.cReload();
                        }
                    },
                }).open();
            }

            if(record.data.LOAI_CHI_PHI_DO_DANG == '1'){
                new dialogs.FormViewDialog(this, {
                    tham_so : dict_param,
                    readonly: false,
                    res_model: 'account.ex.chi.phi.do.dang.master',
                    ref_views: [['account_ex.view_account_ex_chi_phi_do_dang_dtthcp_form', 'form']],
                    title: ("Khai báo chi phí dở dang đầu kỳ cho đối tượng THCP"),
                    disable_multiple_selection: true,
                    save_raw_changes: true,
                    on_after_saved: function (record, changed) {
                        if (changed) {
                            self.load_chi_phi_do_dang();
                            self.changeFieldValue('IS_CHI_TIET',record.data.NHAP_CHI_TIET_LOAI_CPDD_DTTHCP)
                        }
                    },
                }).open();
            }

            if(record.data.LOAI_CHI_PHI_DO_DANG == '2'){
                new dialogs.FormViewDialog(this, {
                    tham_so : dict_param,
                    readonly: false,
                    res_model: 'account.ex.chi.phi.do.dang.master',
                    ref_views: [['account_ex.view_account_ex_chi_phi_do_dang_cong_trinh_form', 'form']],
                    title: ("Nhập lũy kế chi phí phát sinh cho công trình kỳ trước"),
                    disable_multiple_selection: true,
                    save_raw_changes: true,
                    on_after_saved: function (record, changed) {
                        if (changed) {
                            self.load_chi_phi_do_dang();
                            self.changeFieldValue('IS_CHI_TIET',record.data.NHAP_CHI_TIET_LOAI_CPDD_CONG_TRINH)
                        }
                    },
                }).open();
            }

            if(record.data.LOAI_CHI_PHI_DO_DANG == '3'){
                new dialogs.FormViewDialog(this, {
                    tham_so : dict_param,
                    readonly: false,
                    res_model: 'account.ex.chi.phi.do.dang.master',
                    ref_views: [['account_ex.view_account_ex_chi_phi_do_dang_don_hang_form', 'form']],
                    title: ("Nhập lũy kế chi phí phát sinh cho đơn hàng kỳ trước"),
                    disable_multiple_selection: true,
                    save_raw_changes: true,
                    on_after_saved: function (record, changed) {
                        if (changed) {
                            self.load_chi_phi_do_dang();
                            self.changeFieldValue('IS_CHI_TIET',record.data.NHAP_CHI_TIET_LOAI_CPDD_DON_HANG)
                        }
                    },
                }).open();
            }

            if(record.data.LOAI_CHI_PHI_DO_DANG == '4'){
                new dialogs.FormViewDialog(this, {
                    tham_so : dict_param,
                    readonly: false,
                    res_model: 'account.ex.chi.phi.do.dang.master',
                    ref_views: [['account_ex.view_account_ex_chi_phi_do_dang_hop_dong_form', 'form']],
                    title: ("Nhập lũy kế chi phí phát sinh cho hợp đồng kỳ trước"),
                    disable_multiple_selection: true,
                    save_raw_changes: true,
                    on_after_saved: function (record, changed) {
                        if (changed) {
                            self.load_chi_phi_do_dang();
                            self.changeFieldValue('IS_CHI_TIET',record.data.NHAP_CHI_TIET_LOAI_CPDD_HOP_DONG)
                        }
                    },
                }).open();
            }

            if(record.data.KHOAN_MUC_CP_ID){
                new dialogs.FormViewDialog(this, {
                    readonly: false,
                           res_model: 'account.ex.chi.phi.do.dang.master',
                           ref_views: [['account_ex.view_account_ex_chi_phi_chung_can_phan_bo_form', 'form']],
                           title: ("Khai báo chi phí chung cần phân bổ"),
                           disable_multiple_selection: true,
                           on_after_saved: function (record, changed) {
                            if (changed) {
                                self.load_chi_phi_do_dang();
                            }
                        },
                }).open();
            }
             return def; 
            
            
        },


        _onButtonClicked: function(event) {
            var self = this;
			event.stopPropagation();
            switch (event.data.attrs.name)
            {
                case "btn_nhap_so_du_kh":
                    return new dialogs.FormViewDialog(this, _.extend({}, this.nodeOptions, {
                        tham_so : {
                            'ct_theo_dt' : 1,
                            'loai_doi_tuong' : "1",
                            'loai_tien_so_so_cong_no_khach_hang_id' : this.getFieldValue('LOAI_TIEN_ID_SO_CONG_NO_KHACH_HANG'),
                        },
                        readonly: false,
                        res_model: 'account.ex.so.du.tai.khoan',
                        ref_views: [['account_ex.view_account_ex_cong_no_khach_hang_form', 'form']],
                        title: ("Nhập số công nợ khách hàng"),
                        disable_multiple_selection: true,
                        on_after_saved: function (record, changed) {
                            if (changed) {
                                self.cReload();
                            }
                        },
                        
                    })).open();
                    break;

                case "btn_nhap_so_du_tknh":
                    var loai_tien;
                    if(this.getFieldValue('LOAI_TIEN_ID_SO_DU_TK_NGAN_HANG')){
                        loai_tien = this.getFieldValue('LOAI_TIEN_ID_SO_DU_TK_NGAN_HANG');
                    }
                    return new dialogs.FormViewDialog(this, _.extend({}, this.nodeOptions, {
                        tham_so : {
                            'ct_theo_tk' : 1,
                            'loai_tien_so_du_tai_khoan_ngan_hang_id' : loai_tien,
                        },
                        readonly: false,
                        res_model: 'account.ex.so.du.tai.khoan',
                        ref_views: [['account_ex.view_account_ex_so_du_tai_ngan_hang_khoan_form', 'form']],
                        title: ("Nhập số dư tài khoản ngân hàng"),
                        disable_multiple_selection: true,
                        on_after_saved: function (record, changed) {
                            if (changed) {
                                self.cReload();
                            }
                        },
                        
                    })).open();
                    break;

                case "btn_nhap_so_du_ncc":
                    var loai_tien_so_so_cong_no_nha_cung_cap_id;
                    if(this.getFieldValue('LOAI_TIEN_ID_SO_CONG_NO_KHACH_HANG')){
                        loai_tien_so_so_cong_no_nha_cung_cap_id = this.getFieldValue('LOAI_TIEN_ID_SO_CONG_NO_KHACH_HANG');
                    }
                    return new dialogs.FormViewDialog(this, _.extend({}, this.nodeOptions, {
                        tham_so : {
                            'ct_theo_dt' : 1,
                            'loai_doi_tuong' : "0",
                            'loai_tien_so_so_cong_no_nha_cung_cap_id' : loai_tien_so_so_cong_no_nha_cung_cap_id,
                        },
                        readonly: false,
                        res_model: 'account.ex.so.du.tai.khoan',
                        ref_views: [['account_ex.view_account_ex_cong_no_ncc_form', 'form']],
                        title: ("Nhập số dư công nợ nhà cung cấp"),
                        disable_multiple_selection: true,
                        on_after_saved: function (record, changed) {
                            if (changed) {
                                self.cReload();
                            }
                        },
                        
                    })).open();
                    break;

                case "btn_nhap_so_du_nv":
                    var loai_tien_so_so_cong_no_nhan_vien_id;
                    if(this.getFieldValue('LOAI_TIEN_ID_SO_CONG_NO_NHAN_VIEN')){
                        loai_tien_so_so_cong_no_nhan_vien_id = this.getFieldValue('LOAI_TIEN_ID_SO_CONG_NO_KHACH_HANG');
                    }
                    return new dialogs.FormViewDialog(this, _.extend({}, this.nodeOptions, {
                        tham_so : {
                            'ct_theo_dt' : 1,
                            'loai_doi_tuong' : "2",
                            'loai_tien_so_so_cong_no_nhan_vien_id' : loai_tien_so_so_cong_no_nhan_vien_id,
                        },
                        readonly: false,
                        res_model: 'account.ex.so.du.tai.khoan',
                        ref_views: [['account_ex.view_account_ex_cong_no_nhan_vien_form', 'form']],
                        title: ("Nhập số dư công nợ nhân viên"),
                        disable_multiple_selection: true,
                        on_after_saved: function (record, changed) {
                            if (changed) {
                                self.cReload();
                            }
                        },
                        
                    })).open();
                    break;

                case "btn_nhap_so_du_vthh":
                    return new dialogs.FormViewDialog(this, _.extend({}, this.nodeOptions, {
                        tham_so : {
                            'chi_tiet_vthh' : 1,
                        },
                        readonly: false,
                        res_model: 'account.ex.ton.kho.vat.tu.hang.hoa.master',
                        ref_views: [['account_ex.view_account_ex_ton_kho_vat_tu_hang_hoa_master_form', 'form']],
                        title: ("Nhập tồn kho vật tư, hàng hóa"),
                        disable_multiple_selection: true,
                        on_after_saved: function (record, changed) {
                            if (changed) {
                                self.cReload();
                            }
                        },
                        
                    })).open();
                    break;

                case "btn_nhap_chi_phi_cpdd":
                    var chi_phi_do_dang = this.getFieldValue('chi_phi_do_dang');
                    if(chi_phi_do_dang=='DT_THCP') {
                     return new dialogs.FormViewDialog(this, _.extend({}, this.nodeOptions, {
                        tham_so : {
                            'chi_tiet_vthh' : 1,
                        },
                        readonly: false,
                        res_model: 'account.ex.chi.phi.do.dang.master',
                        ref_views: [['account_ex.view_account_ex_chi_phi_do_dang_dtthcp_form', 'form']],
                        title: ("Khai báo chi phí dở dang đầu kỳ cho đối tượng THCP"),
                        disable_multiple_selection: true,
                        on_after_saved: function (record, changed) {
                            if (changed) {
                                self.load_chi_phi_do_dang();
                                self.changeFieldValue('IS_CHI_TIET',record.data.NHAP_CHI_TIET_LOAI_CPDD_DTTHCP)
                            }
                        },
                        
                    })).open();

                    }
                    if(chi_phi_do_dang=='CONG_TRINH') {
                     return new dialogs.FormViewDialog(this, _.extend({}, this.nodeOptions, {
                        tham_so : {
                            'chi_tiet_vthh' : 1,
                        },
                        readonly: false,
                        res_model: 'account.ex.chi.phi.do.dang.master',
                        ref_views: [['account_ex.view_account_ex_chi_phi_do_dang_cong_trinh_form', 'form']],
                        title: ("Nhập lũy kế chi phí phát sinh cho công trình kỳ trước"),
                        disable_multiple_selection: true,
                        on_after_saved: function (record, changed) {
                            if (changed) {
                                self.load_chi_phi_do_dang();
                                self.changeFieldValue('IS_CHI_TIET',record.data.NHAP_CHI_TIET_LOAI_CPDD_CONG_TRINH)
                            }
                        },
                        
                    })).open();

                    }
                    if(chi_phi_do_dang=='DON_HANG') {
                        return new dialogs.FormViewDialog(this, _.extend({}, this.nodeOptions, {
                           tham_so : {
                               'chi_tiet_vthh' : 1,
                           },
                           readonly: false,
                           res_model: 'account.ex.chi.phi.do.dang.master',
                           ref_views: [['account_ex.view_account_ex_chi_phi_do_dang_don_hang_form', 'form']],
                           title: ("Nhập lũy kế chi phí phát sinh cho đơn hàng kỳ trước"),
                           disable_multiple_selection: true,
                           on_after_saved: function (record, changed) {
                            if (changed) {
                                self.load_chi_phi_do_dang();
                                self.changeFieldValue('IS_CHI_TIET',record.data.NHAP_CHI_TIET_LOAI_CPDD_DON_HANG)
                            }
                        },
                           
                       })).open();
   
                       }
                       if(chi_phi_do_dang=='CHI_PHI_PB') {
                        return new dialogs.FormViewDialog(this, _.extend({}, this.nodeOptions, {
                           tham_so : {
                               'chi_tiet_vthh' : 1,
                           },
                           readonly: false,
                           res_model: 'account.ex.chi.phi.do.dang.master',
                           ref_views: [['account_ex.view_account_ex_chi_phi_chung_can_phan_bo_form', 'form']],
                           title: ("Khai báo chi phí chung cần phân bổ"),
                           disable_multiple_selection: true,
                           on_after_saved: function (record, changed) {
                            if (changed) {
                                self.load_chi_phi_do_dang();
//                                 self.changeFieldValue('IS_CHI_TIET',record.data.NHAP_CHI_TIET_LOAI_CPDD_DON_HANG)
                            }
                        },
                           
                       })).open();
   
                       }

                    if(chi_phi_do_dang=='HOP_DONG') {
                        return new dialogs.FormViewDialog(this, _.extend({}, this.nodeOptions, {
                           tham_so : {
                               'chi_tiet_vthh' : 1,
                           },
                           readonly: false,
                           res_model: 'account.ex.chi.phi.do.dang.master',
                           ref_views: [['account_ex.view_account_ex_chi_phi_do_dang_hop_dong_form', 'form']],
                           title: ("Nhập lũy kế chi phí phát sinh cho hợp đồng kỳ trước"),
                           disable_multiple_selection: true,
                           on_after_saved: function (record, changed) {
                            if (changed) {
                                self.load_chi_phi_do_dang();
                                self.changeFieldValue('IS_CHI_TIET',record.data.NHAP_CHI_TIET_LOAI_CPDD_HOP_DONG)
                            }
                        },
                           
                       })).open();
   
                       }
                   
                    break;
                
                default: 
                   this._super.apply(this, arguments);
            }
           
            
        },
      
        onViewLoaded: function(e, defer) {
            this.cReload(defer);
        },

        

        cReload:function(defer) {
            var def = defer;
            var self = this;
            self.changeFieldValue('KHO_ID', -1);
            this.rpc_action({
                model: 'account.ex.nhap.so.du.ban.dau',
                method: 'load_form',
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

        load_chi_phi_do_dang:function(defer) {
            var def = defer;
            var self = this;
            var loai_cpdd = this.getFieldValue('chi_phi_do_dang');
            this.rpc_action({
                model: 'account.ex.nhap.so.du.ban.dau',
                method: 'lay_du_lieu_cpdd',
                args: {'loai_cpdd' : loai_cpdd},
                callback: function(result) {
                    if (result) {
                        self.updateUI(result);
                        }   
                    }
                });
        },

        onFieldChanged: function(field){
            var loai_tien_id = -1;
            if(this.getFieldValue(field)){
                loai_tien_id = this.getFieldValue(field).id;
            }
            var self = this;
            if(field =="LOAI_TIEN_ID_SO_DU_TAI_KHOAN")
            {
                this.rpc_action({
                    model: 'account.ex.nhap.so.du.ban.dau',
                    method: 'lay_du_tai_khoan_ui',
                    args: {'id_loai_tien':loai_tien_id},
                    callback: function(result) {
                        if (result) {
                            self.updateUI(result);
                            }   
                        }
                    });
            }
            if(field =="LOAI_TIEN_ID_SO_DU_TK_NGAN_HANG")
            {
                this.rpc_action({
                    model: 'account.ex.nhap.so.du.ban.dau',
                    method: 'lay_so_du_tai_khoan_ngan_hang_ui',
                    args: {'id_loai_tien':loai_tien_id},
                    callback: function(result) {
                        if (result) {
                            self.updateUI(result);
                            }   
                        }
                    });
            }
            if(field =="LOAI_TIEN_ID_SO_CONG_NO_KHACH_HANG")
            {
                this.rpc_action({
                    model: 'account.ex.nhap.so.du.ban.dau',
                    method: 'lay_cong_no_khach_hang_ui',
                    args: {'id_loai_tien':loai_tien_id},
                    callback: function(result) {
                        if (result) {
                            self.updateUI(result);
                            }   
                        }
                    });
            }
            if(field =="LOAI_TIEN_ID_SO_CONG_NO_NHA_CUNG_CAP")
            {
                this.rpc_action({
                    model: 'account.ex.nhap.so.du.ban.dau',
                    method: 'lay_cong_no_nha_cung_cap_ui',
                    args: {'id_loai_tien':loai_tien_id},
                    callback: function(result) {
                        if (result) {
                            self.updateUI(result);
                            }   
                        }
                    });
            }
            if(field =="LOAI_TIEN_ID_SO_CONG_NO_NHAN_VIEN")
            {
                this.rpc_action({
                    model: 'account.ex.nhap.so.du.ban.dau',
                    method: 'lay_cong_no_nhan_vien_ui',
                    args: {'id_loai_tien':loai_tien_id},
                    callback: function(result) {
                        if (result) {
                            self.updateUI(result);
                            }   
                        }
                    });
            }

            if(field =="chi_phi_do_dang")
            {
                self.load_chi_phi_do_dang();
            };

            if(field =="KHO_ID")
            {
                var kho_id = -1;
                if(this.getFieldValue('KHO_ID')){
                    kho_id = this.getFieldValue('KHO_ID').id
                }
                this.rpc_action({
                    model: 'account.ex.ton.kho.vat.tu.hang.hoa.master',
                    method: 'ton_kho_vat_tu_hang_hoa',
                    args: {'kho_id' : kho_id},
                    callback: function(result) {
                        if (result) {
                            self.updateUI(result);
                            }   
                        }
                    });
            }
            
        }
    });
    
    var SoDuBanDauView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: SoDuBanDauController,
        }),
    });
    
    view_registry.add('account_ex_so_du_ban_dau_form_view', SoDuBanDauView);
    
    return SoDuBanDauView;
});