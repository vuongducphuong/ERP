odoo.define('gia_thanh.ky_tinh_gia_thanh_hop_dong_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var KyTinhGiaThanhHopDongFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        _onButtonClicked: function(event) {
            
            event.stopPropagation();
            var self = this;
            switch (event.data.attrs.id)
            {
                case "btn_phan_bo_chi_phi_chung":
                    var ten = this.getFieldValue('TEN');
                    var ky_tinh_gia_thanh_id = event.data.record.data.id;
                    new dialogs.FormViewDialog(this, {
                        tham_so : ten,
                        ky_tinh_gia_thanh_id : ky_tinh_gia_thanh_id,
                        readonly: false,
                        res_model: 'gia.thanh.tinh.gia.thanh',
                        ref_views: [['gia_thanh.view_gia_thanh_phan_bo_chi_phi_chung_hop_dong_form', 'form']],
                        title: 'Phân bổ chi phí chung',
                        disable_multiple_selection: true,
                        shouldSaveLocally: false,
                        // on_saved: function (record, changed) {
                                //     if (changed) {
                                //         self.cReload();
                                //     }
                                // },
                    }).open();
                    break;
                case "btn_tap_hop_chi_phi_truc_tiep":
                    var ten = this.getFieldValue('TEN');
                    var ky_tinh_gia_thanh_id = event.data.record.data.id;
                    new dialogs.FormViewDialog(this, {
                        tham_so : ten,
                        ky_tinh_gia_thanh_id : ky_tinh_gia_thanh_id,
                        readonly: false,
                        res_model: 'gia.thanh.tap.hop.chi.phi.truc.tiep',
                        ref_views: [['gia_thanh.view_gia_thanh_tap_hop_chi_phi_truc_tiep_hop_dong_tham_so_form', 'form']],
                        title: 'Tập hợp chi phí trực tiếp',
                        disable_multiple_selection: true,
                        shouldSaveLocally: true,
                        // on_saved: function (record, changed) {
                                //     if (changed) {
                                //         self.cReload();
                                //     }
                                // },
                    }).open();
                    break;
                case "btn_tap_hop_khoan_giam_gia_thanh":
                    var ten = this.getFieldValue('TEN');
                    var ky_tinh_gia_thanh_id = event.data.record.data.id;
                    new dialogs.FormViewDialog(this, {
                        tham_so : ten,
                        ky_tinh_gia_thanh_id : ky_tinh_gia_thanh_id,
                        readonly: false,
                        res_model: 'gia.thanh.tap.hop.khoan.giam.gia.thanh',
                        ref_views: [['gia_thanh.view_gia_thanh_tap_hop_khoan_giam_gia_thanh_hop_dong_tham_so_form', 'form']],
                        title: 'Tập hợp khoản giảm giá thành',
                        disable_multiple_selection: true,
                        shouldSaveLocally: true,
                        // on_saved: function (record, changed) {
                                //     if (changed) {
                                //         self.cReload();
                                //     }
                                // },
                    }).open();
                    break;
                case "btn_bang_tap_hop_chi_phi_theo_yeu_to":
                    var ten = this.getFieldValue('TEN');
                    var ky_tinh_gia_thanh_id = event.data.record.data.id;
                    new dialogs.FormViewDialog(this, {
                        tham_so : ten,
                        ky_tinh_gia_thanh_id : ky_tinh_gia_thanh_id,
                        readonly: false,
                        res_model: 'gia.thanh.bang.tap.hop.chi.phi.theo.yeu.to',
                        ref_views: [['gia_thanh.view_gia_thanh_bang_tap_hop_chi_phi_theo_yeu_to_hop_dong_tham_so_form', 'form']],
                        title: 'Bảng tập hợp chi phí theo yếu tố',
                        disable_multiple_selection: true,
                        shouldSaveLocally: true,
                        // on_saved: function (record, changed) {
                                //     if (changed) {
                                //         self.cReload();
                                //     }
                                // },
                    }).open();
                    break;
                case "btn_bang_tap_hop_chi_phi_theo_khoan_muc":
                    var ten = this.getFieldValue('TEN');
                    var ky_tinh_gia_thanh_id = event.data.record.data.id;
                    new dialogs.FormViewDialog(this, {
                        tham_so : ten,
                        ky_tinh_gia_thanh_id : ky_tinh_gia_thanh_id,
                        readonly: false,
                        res_model: 'gia.thanh.bang.tap.hop.chi.phi.theo.khoan.muc',
                        ref_views: [['gia_thanh.view_gia_thanh_bang_tap_hop_chi_phi_theo_khoan_muc_hop_dong_tham_so_form', 'form']],
                        title: 'Bảng tập hợp chi phí theo khoản mục',
                        disable_multiple_selection: true,
                        shouldSaveLocally: true,
                        // on_saved: function (record, changed) {
                                //     if (changed) {
                                //         self.cReload();
                                //     }
                                // },
                    }).open();
                    break;
                case "btn_ket_chuyen_chi_phi":
                    var ky_tinh_gia_thanh_id = event.data.record.data.id;
                    var context = {
                        'ten': this.getFieldValue('TEN'),
                        'tu_ngay':this.getFieldValue('TU_NGAY'),
                        'den_ngay':this.getFieldValue('DEN_NGAY'),
                        'loai_chung_tu': 4083,
                        'id_ky_tinh_gia_thanh':ky_tinh_gia_thanh_id,
                        };
                    self.rpc_action({
                        model: 'gia.thanh.ky.tinh.gia.thanh',
                        method: 'kiem_tra_ton_tai_ket_chuyen',
                        args: {
                            'id_ky_tinh_gia_thanh':ky_tinh_gia_thanh_id,
                        },
                        callback: function(result) {
                            if (result == 0) {
                                new dialogs.FormViewDialog(self, {
                                    context : context,
                                    ky_tinh_gia_thanh_id : ky_tinh_gia_thanh_id,
                                    form_them_moi : true,
                                    readonly: false,
                                    res_model: 'gia.thanh.ket.chuyen.chi.phi',
                                    ref_views: [['gia_thanh.view_gia_thanh_ket_chuyen_chi_phi_hop_dong_form1', 'form']],
                                    title: 'Kết chuyển chi phí (Hợp đồng)',
                                    disable_multiple_selection: true,
                                    shouldSaveLocally: false,
                                }).open();
                            }
                            else{
                                Dialog.show_message('', 'Đã tồn tại chứng từ kết chuyển chi phí của kỳ tính giá thành này. Bạn có muốn xem chứng từ này không?', 'CONFIRM')
                                .then(function(result_yes_no) {
                                    if (result_yes_no == true){
                                        if (result_yes_no == true){
                                            var options = {
                                                res_model: 'gia.thanh.ket.chuyen.chi.phi',
                                                ref_view: 'gia_thanh.view_gia_thanh_ket_chuyen_chi_phi_hop_dong_form1',
                                                res_id : result,
                                                title: 'Kết chuyển chi phí',
                                            }
                                            return self.openFormView(options);
                                        }
                                    }
                                        // new dialogs.FormViewDialog(self, {
                                        //     // context : context,
                                        //     res_id : result,
                                        //     readonly: false,
                                        //     res_model: 'gia.thanh.ket.chuyen.chi.phi',
                                        //     ref_views: [['gia_thanh.view_gia_thanh_ket_chuyen_chi_phi_hop_dong_form', 'form']],
                                        //     title: 'Kết chuyển chi phí (Hợp đồng)',
                                        //     disable_multiple_selection: true,
                                        //     shouldSaveLocally: false,
                                    
                                        // }).open();
                                });
                    
                        
                            }         
                    }});
                    break;
                case "btn_nghiem_thu_hop_dong":
                    var ky_tinh_gia_thanh_id = event.data.record.data.id;
                    var context = {
                        'ten': this.getFieldValue('TEN'),
                        'id_ky_tinh_gia_thanh': ky_tinh_gia_thanh_id,
                        };
                    new dialogs.FormViewDialog(this, {
                        tham_so : context,
                        ky_tinh_gia_thanh_id : ky_tinh_gia_thanh_id,
                        readonly: false,
                        res_model: 'gia.thanh.chon.ky.tinh.gia.thanh.form',
                        ref_views: [['gia_thanh.view_gia_thanh_chon_ky_tinh_gia_thanh_hop_dong_form_tham_so_form', 'form']],
                        title: 'Chọn kỳ tính giá thành',
                        disable_multiple_selection: true,
                        shouldSaveLocally: true,
                        on_before_saved: function(controller) {
                            var def = $.Deferred();
                            var dem = 0;
                            var error =[];
                            var chi_tiet = controller.getFieldValue('GIA_THANH_CHON_KY_TINH_GIA_THANH_FORM_CHI_TIET_IDS');
                            for (var i= 0 ; i < chi_tiet.length; i++){
                                    if(chi_tiet[i].AUTO_SELECT){
                                            dem = dem + 1;
                                    }
                            }
                            if(dem == 0){
                                error = 'Bạn chưa chọn chi tiết Hợp đồng để thực hiện nghiệm thu';
                                self.notifyInvalidFields(error);
                                def.resolve(false);
                            }
                            def.resolve(true);
                            return def;
                                              
                        },
                        on_after_saved: function(record, changed) {
                            if (changed){
                        
                                var ky_tinh_gia_thanh = record.data.KY_TINH_GIA_THANH;
                                var ky_tinh_gia_thanh_id = record.data.KY_TINH_GIA_THANH_ID.data.id;
                                var chi_tiet_ids = record.data.GIA_THANH_CHON_KY_TINH_GIA_THANH_FORM_CHI_TIET_IDS.data;
                                var den_ngay = self.getFieldValue('DEN_NGAY');
                                var arr_nghiem_thu_cong_trinh_chi_tiet = [];
                                if(chi_tiet_ids && chi_tiet_ids.length > 0){
                                    for(var i =0;i<chi_tiet_ids.length;i++){
                                        var chi_tiet = chi_tiet_ids[i].data;
                                        if(chi_tiet.AUTO_SELECT == true && chi_tiet.SO_CHUA_NGHIEM_THU > 0){
                                            arr_nghiem_thu_cong_trinh_chi_tiet.push(chi_tiet.HOP_DONG_BAN_ID.data.id)
                                        }
                                    }
                                }
                                var context = {
                                    'default_KY_TINH_GIA_THANH': ky_tinh_gia_thanh,
                                    'default_KY_TINH_GIA_THANH_ID': ky_tinh_gia_thanh_id,
                                    'default_NGAY_HACH_TOAN': den_ngay,
                                    'default_NGAY_CHUNG_TU': den_ngay,
                                    'loai_chung_tu': 4092,
                                }
                                new dialogs.FormViewDialog(self, {
                                    // res_id : result,
                                    form_them_moi : true,
                                    params : arr_nghiem_thu_cong_trinh_chi_tiet,
                                    context:context,
                                    readonly: false,
                                    res_model: 'gia.thanh.nghiem.thu',
                                    ref_views: [['gia_thanh.view_gia_thanh_nghiem_thu_hop_dong_form1', 'form']],
                                    title: 'Nghiệm thu hợp đồng',
                                    disable_multiple_selection: true,
                                    shouldSaveLocally: false,
                            
                                }).open();
                
                
                            }
                    }
                    }).open();
                    
                    break;
                case "btn_chon":
                    new dialogs.FormViewDialog(this, {
                        // tham_so : dict_param,
                        readonly: false,
                        res_model: 'gia.thanh.chon.doi.tuong.can.tap.hop.chi.phi.form',
                        ref_views: [['gia_thanh.view_gia_thanh_chon_doi_tuong_can_tap_hop_chi_phi_hop_dong_form', 'form']],
                        title: 'Chọn hợp đồng',
                        size : 'large',
                        disable_multiple_selection: true,
                        shouldSaveLocally: true,
                        on_after_saved: function(record, changes) {
                            if(changes){
                                var default_doi_tuong_thcp  =[[5]];
                                

                                var current_data = record.data;
                                var chitiet_ids = current_data.GIA_THANH_CHON_DOI_TUONG_CAN_TAP_HOP_CHI_PHI_CHI_TIET_IDS.data;
                                for(var i=0;i<chitiet_ids.length;i++)
                                {
                                    
                                    //chỉ lấy những thằng chọn
                                    var chi_tiet = chitiet_ids[i].data;
                                    if (chi_tiet.AUTO_SELECT)
                                    {
                                        default_doi_tuong_thcp.push([0, 0, {
                                            'SO_HOP_DONG_ID': [chi_tiet.SO_HOP_DONG_ID.data.id,chi_tiet.SO_HOP_DONG_ID.data.display_name],
                                            'NGAY_KY': chi_tiet.NGAY_HOP_DONG ,
                                            'TRICH_YEU': chi_tiet.TRICH_YEU,
                                            'KHACH_HANG_HOP_DONG': chi_tiet.KHACH_HANG,
                                    }])
                                    }

                                }
                                self.updateUI({'GIA_THANH_KY_TINH_GIA_THANH_CHI_TIET_IDS':default_doi_tuong_thcp,});

    
                        }
                    }
                    }).open();
                    break;
                default: 
                   this._super.apply(this, arguments);
            }
            
        },
    });

    var KyTinhGiaThanhHopDongFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: KyTinhGiaThanhHopDongFormController,
        }),
    });
    
    view_registry.add('ky_tinh_gia_thanh_hop_dong_view', KyTinhGiaThanhHopDongFormView);
    
    return KyTinhGiaThanhHopDongFormView;
});
