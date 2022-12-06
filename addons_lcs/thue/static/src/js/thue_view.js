odoo.define('thue.thue_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var ThueFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        _onCreate: function(context) {
            var self = this;
            // var domain_san_xuat_lien_tuc_gian_don ='CONG_TRINH';
            new dialogs.FormViewDialog(this, {
                tham_so:context,
                readonly: false,
                res_model: 'thue.chon.ky.tinh.thue',
                ref_views: [['thue.view_thue_chon_ky_tinh_thue_tham_so_form', 'form']],
                title: ("Chọn kỳ tính thuế"),
                disable_multiple_selection: true,
                size : 'large',
                shouldSaveLocally: true,
                on_after_saved: function (record, changed) {
                    if (changed) {
                        var default_phu_luc_ke_khai  =[[5]];
                        var current_data = record.data;
                        var chitiet_ids = current_data.THUE_PHU_LUC_KE_KHAI_IDS.data;
                        for(var i=0;i<chitiet_ids.length;i++)
                        {
                            //chỉ lấy những thằng chọn
                            var chi_tiet = chitiet_ids[i].data;
                            if (chi_tiet.AUTO_SELECT)
                            {
                                default_phu_luc_ke_khai.push([0, 0, {
                                    'MA_PHU_LUC': chi_tiet.MA_PHU_LUC,
                                 }])
                            }

                        }
                        var context = {
                            'default_THUE_PHU_LUC_KE_KHAI_IDS': default_phu_luc_ke_khai,
                            'default_khoan_muc_thue':record.data.KHOAN_MUC_THUE,
                            'default_loai_to_khai':record.data.LOAI_TO_KHAI,
                            'default_hang_muc_khai':record.data.HANG_MUC_KHAI,
                            'default_thang':record.data.THANG,
                            'default_quy':record.data.QUY,
                            'default_nam':record.data.NAM,
                            'default_lan_khai_bo_sung':record.data.LAN_KHAI,
                            'default_ngay':record.data.NGAY,
                        }
                        self.createRecord(context);
                    }
                },
            }).open();
            
        },
        _onButtonClicked: function(event) {
            event.stopPropagation();
            var self = this;
            switch (event.data.attrs.id)
            {
                case "btn_xem_chi_tiet":
                    return new dialogs.FormViewDialog(this, _.extend({}, this.nodeOptions, {
                        readonly: false,
                        res_model: 'thue.chung.tu.khong.hop.le',
                        ref_views: [['thue.view_thue_chung_tu_khong_hop_le_tham_so_form', 'form']],
                        title: ("Danh sách chứng từ không hợp lệ"),
                        disable_multiple_selection: true,
                        size : 'large',
                        shouldSaveLocally: true,
                        // on_after_saved: function (record, changed) {
                        //     if (changed) {
                        //         // var ky_tinh_gia_thanh = record.data.KY_TINH_GIA_THANH_ID.data.display_name;
                        //         // var ky_tinh_gia_thanh_id = record.data.KY_TINH_GIA_THANH_ID.data.id;
                        //         // var ngay_hach_toan = record.data.DEN_NGAY
                        //         var context = {
                                    
                        //         }
                        //         self.createRecord(context);
                        //     }
                        // },
                    })).open();
                    break;
                case "btn_xem_chi_tiet_pl012":
                    return new dialogs.FormViewDialog(this, _.extend({}, this.nodeOptions, {
                        readonly: false,
                        res_model: 'thue.chung.tu.khong.hop.le',
                        ref_views: [['thue.view_thue_chung_tu_khong_hop_le_tham_so_pl012_gtgt_form', 'form']],
                        title: ("Danh sách chứng từ không hợp lệ"),
                        disable_multiple_selection: true,
                        size : 'large',
                        shouldSaveLocally: true,
                        // on_after_saved: function (record, changed) {
                        //     if (changed) {
                        //         // var ky_tinh_gia_thanh = record.data.KY_TINH_GIA_THANH_ID.data.display_name;
                        //         // var ky_tinh_gia_thanh_id = record.data.KY_TINH_GIA_THANH_ID.data.id;
                        //         // var ngay_hach_toan = record.data.DEN_NGAY
                        //         var context = {
                                    
                        //         }
                        //         self.createRecord(context);
                        //     }
                        // },
                    })).open();
                    break;
                case "btn_xem_chi_tiet_plbkbr":
                    return new dialogs.FormViewDialog(this, _.extend({}, this.nodeOptions, {
                        readonly: false,
                        res_model: 'thue.chung.tu.khong.hop.le',
                        ref_views: [['thue.view_thue_chung_tu_khong_hop_le_tham_so_plbkbr_ttdb_form', 'form']],
                        title: ("Danh sách chứng từ không hợp lệ"),
                        disable_multiple_selection: true,
                        size : 'large',
                        shouldSaveLocally: true,
                        // on_after_saved: function (record, changed) {
                        //     if (changed) {
                        //         // var ky_tinh_gia_thanh = record.data.KY_TINH_GIA_THANH_ID.data.display_name;
                        //         // var ky_tinh_gia_thanh_id = record.data.KY_TINH_GIA_THANH_ID.data.id;
                        //         // var ngay_hach_toan = record.data.DEN_NGAY
                        //         var context = {
                                    
                        //         }
                        //         self.createRecord(context);
                        //     }
                        // },
                    })).open();
                    break;
            default: 
        this._super.apply(this, arguments);
            }
        },
        
    });
    
    var ThueFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
           
            Controller: ThueFormController,
        }),
    });
    
    view_registry.add('thue_form_view', ThueFormView);
    
    return ThueFormView;
});
odoo.define('thue.thue_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var ThueController = ListController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        _onCreate: function(context) {
            var self = this;
            // var domain_san_xuat_lien_tuc_gian_don ='CONG_TRINH';
            new dialogs.FormViewDialog(this, {
                tham_so:context,
                readonly: false,
                res_model: 'thue.chon.ky.tinh.thue',
                ref_views: [['thue.view_thue_chon_ky_tinh_thue_tham_so_form', 'form']],
                title: ("Chọn kỳ tính thuế"),
                disable_multiple_selection: true,
                size : 'large',
                shouldSaveLocally: true,
                on_after_saved: function (record, changed) {
                    if (changed) {
                        var default_phu_luc_ke_khai  =[[5]];
                        var current_data = record.data;
                        var chitiet_ids = current_data.THUE_PHU_LUC_KE_KHAI_IDS.data;
                        for(var i=0;i<chitiet_ids.length;i++)
                        {
                            //chỉ lấy những thằng chọn
                            var chi_tiet = chitiet_ids[i].data;
                            if (chi_tiet.AUTO_SELECT)
                            {
                                default_phu_luc_ke_khai.push([0, 0, {
                                    'MA_PHU_LUC': chi_tiet.MA_PHU_LUC,
                                 }])
                            }

                        }
                        var context = {
                            'default_THUE_PHU_LUC_KE_KHAI_IDS': default_phu_luc_ke_khai,
                            'default_khoan_muc_thue':record.data.KHOAN_MUC_THUE,
                            'default_loai_to_khai':record.data.LOAI_TO_KHAI,
                            'default_hang_muc_khai':record.data.HANG_MUC_KHAI,
                            'default_thang':record.data.THANG,
                            'default_quy':record.data.QUY,
                            'default_nam':record.data.NAM,
                            'default_lan_khai_bo_sung':record.data.LAN_KHAI,
                            'default_ngay':record.data.NGAY,
                        }
                        self.createRecord(context);
                    }
                },
            }).open();
            
        },
        
    });
    
    var ThueView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: ThueController,
        }),
    });
    
    view_registry.add('thue_list_view', ThueView);
    
    return ThueView;
});
