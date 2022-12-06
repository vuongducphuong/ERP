odoo.define('gia_thanh.nghiem_thu_hop_dong_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');


    var NghiemThuHopDongFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        onViewLoaded: function(e, defer) {
            var self = this;
			var def =  defer;
			if (self.params && self.params.context ){                
                self.updateUI({'KY_TINH_GIA_THANH':self.params.context.default_KY_TINH_GIA_THANH,'LOAI_CHUNG_TU': 4092});
            }
            if(self.params && self.params.form_them_moi == true){
                this.rpc_action({
                    model: 'gia.thanh.nghiem.thu',
                    method: 'lay_du_lieu_nghiep_thu_chi_tiet',
                    args: {
                        'arr_chi_tiet_id' : self.params.params,
                        'ky_tinh_gia_thanh_id' : self.params.context.default_KY_TINH_GIA_THANH_ID,
                        'loai_nghiem_thu' : 'hop_dong',
                    },
                    callback: function(result) {
                        if (result) {
                            self.updateUI(result);
                        }
                    }
                });
            }
            def.resolve();
        },
        _onCreate: function() {
            var self = this;
            var domain_hop_dong ='HOP_DONG';
            new dialogs.FormViewDialog(this, {
                tham_so: domain_hop_dong,
                readonly: false,
                res_model: 'gia.thanh.chon.ky.tinh.gia.thanh.form',
                ref_views: [['gia_thanh.view_gia_thanh_chon_ky_tinh_gia_thanh_hop_dong_form_tham_so_form1', 'form']],
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
                on_after_saved: function (record, changed) {
                    if (changed){
                        
                        var ky_tinh_gia_thanh = record.data.KY_TINH_GIA_THANH_ID.data.display_name;
                        var ky_tinh_gia_thanh_id = record.data.KY_TINH_GIA_THANH_ID.data.id;
                    
                        var context = {
                            'default_KY_TINH_GIA_THANH': ky_tinh_gia_thanh,
                            'default_KY_TINH_GIA_THANH_ID': ky_tinh_gia_thanh_id,
                            'loai_chung_tu': 4092,
                        }
                        new dialogs.FormViewDialog(self, {
                            // res_id : result,
                            context:context,
                            readonly: false,
                            res_model: 'gia.thanh.nghiem.thu',
                            ref_views: [['gia_thanh.view_gia_thanh_nghiem_thu_hop_dong_form', 'form']],
                            title: 'Nghiệm thu hợp đồng',
                            disable_multiple_selection: true,
                            shouldSaveLocally: false,
                    
                        }).open();
        
        
                    }
                }
            }).open();
        },
        _onButtonClicked: function(event) {
            event.stopPropagation();
            var self = this;
            switch (event.data.attrs.id)
            {
                case "btn_duyet":
                    new dialogs.FormViewDialog(this, {
                        // tham_so : dict_param,
                        readonly: false,
                        res_model: 'gia.thanh.danh.sach.ket.chuyen.chi.phi',
                        ref_views: [['gia_thanh.view_gia_thanh_danh_sach_ket_chuyen_chi_phi_tham_so_form', 'form']],
                        title: ("Danh sách nghiệm thu hợp đồng"),
                        disable_multiple_selection: true,
                        shouldSaveLocally: true,
                    }).open();
                    break;
                default: 
                   this._super.apply(this, arguments);
            }
            
        },
    });
    
    var NghiemThuHopDongFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
           
            Controller: NghiemThuHopDongFormController,
        }),
    });
    
    view_registry.add('nghiem_thu_hop_dong_form_view', NghiemThuHopDongFormView);
    
    return NghiemThuHopDongFormView;
});
odoo.define('gia_thanh.nghiem_thu_hop_dong_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var NghiemThuHopDongController = ListController.extend({
       _onCreate: function() {
            var self = this;
            var domain_hop_dong ='HOP_DONG';
            new dialogs.FormViewDialog(this, {
                tham_so: domain_hop_dong,
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
                on_after_saved: function (record, changed) {
                    if (changed){
                        
                        var ky_tinh_gia_thanh = record.data.KY_TINH_GIA_THANH_ID.data.display_name;
                        var ky_tinh_gia_thanh_id = record.data.KY_TINH_GIA_THANH_ID.data.id;
                        var chi_tiet_ids = record.data.GIA_THANH_CHON_KY_TINH_GIA_THANH_FORM_CHI_TIET_IDS.data;
                        var den_ngay = record.data.DEN_NGAY;
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
        },
    });
    
    var NghiemThuHopDongView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: NghiemThuHopDongController,
        }),
    });
    
    view_registry.add('nghiem_thu_hop_dong_list_view', NghiemThuHopDongView);
    
    return NghiemThuHopDongView;
});
