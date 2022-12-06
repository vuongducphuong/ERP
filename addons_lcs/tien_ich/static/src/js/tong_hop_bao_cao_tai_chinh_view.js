odoo.define('tong_hop.tong_hop_bao_cao_tai_chinh_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var BaoCaoTaiChinhController = FormController.extend({
        _onCreate: function () {
            var self = this;
            new dialogs.FormParamsDialog(this, _.extend({}, this.nodeOptions, {
                res_model: 'tong.hop.lap.bao.cao.tai.chinh',
                title: 'Chọn tham số báo cáo:Báo cáo tài chính',
                ref_views: [['tong_hop.view_tong_hop_bao_cao_tai_chinh_form', 'form']],
                on_selected: function (params,handle) {
                    var context = {
                        'default_KY': params.KY,
                        'default_NAM': params.NAM,
                        'default_DOANH_NGHIEP_SELECTION': params.DOANH_NGHIEP_SELECTION,
                        'default_TU': params.TU,
                        'default_DEN': params.DEN,
                    };
                    var default_chi_tiet = [];
                    // Lấy data hiện tại của form
                    //var current_data = event.data.record.data;
                    // Lấy data của chứng từ chi tiết
                    var chi_tiet_ids = params.TONG_HOP_LAP_BAO_CAO_TAI_CHINH_CHI_TIET_IDS;
                    for (var i=0; i< chi_tiet_ids.length; i++) {
                        var chi_tiet = chi_tiet_ids[i];
                    
                            default_chi_tiet.push( {
                                'AUTO_SELECT': chi_tiet.AUTO_SELECT,
                                'MA_BAO_CAO_ID': chi_tiet.MA_BAO_CAO_ID,
                                'MA_PHU_LUC_ID': chi_tiet.MA_BAO_CAO_ID,
                                'TEN_PHU_LUC': chi_tiet.TEN_BAO_CAO,

                            });
                        
                        
                    }
                    context['default_LAY_DU_LIEU_THAM_SO'] = default_chi_tiet;

                    self.createRecord(context);
                    self.closeDialog(handle);

                },
            })).open();
        },

        _onButtonClicked: function(event) {
            var self = this;
			event.stopPropagation();
            switch (event.data.attrs.id)
            {
                
                case "btn_kiem_tra":
                    return new dialogs.SelectParamsDialog(this, _.extend({}, this.nodeOptions, {
                        res_model: 'tong.hop.bctc.kiem.tra.bang.ke.toan.khong.can.form',
                        title: 'Kiểm tra nguyên nhân Bảng cân đối kế toán không cân',
                        ref_views: [['tong_hop.view_tong_hop_bctc_kiem_tra_bang_ke_toan_khong_can_form_tham_so_form', 'form']],
                        // context: _.extend(event.data.record.context || {}, event.data.record.data || {}),
                        on_selected: function () {
                           
                            
                        },
                    })).open();
                    break;

                case "btn_chon_nghiep_vu_cho_cac_chung_tu":
                    return new dialogs.SelectParamsDialog(this, _.extend({}, this.nodeOptions, {
                        res_model: 'tong.hop.bctc.chon.nghiep.vu.cho.cac.chung.tu.form',
                        title: 'Chọn nghiệp vụ cho các chứng từ',
                        ref_views: [['tong_hop.view_tong_hop_bctc_chon_nghiep_vu_cho_cac_chung_tu_form_tham_so_form', 'form']],
                        // context: _.extend(event.data.record.context || {}, event.data.record.data || {}),
                        on_selected: function () {
                           
                            
                        },
                    })).open();
                    break;
                    
                case "btn_chon_hoat_dong_lctt":
                    return new dialogs.SelectParamsDialog(this, _.extend({}, this.nodeOptions, {
                        res_model: 'tong.hop.bctc.chon.lai.hoat.dong.lctt.form',
                        title: 'XÁC ĐỊNH HOẠT ĐỘNG LƯU CHUYỂN TIỀN TỆ CỦA CHỨNG TỪ ',
                        ref_views: [['tong_hop.view_tong_hop_bctc_chon_lai_hoat_dong_lctt_form_tham_so_form', 'form']],
                        // context: _.extend(event.data.record.context || {}, event.data.record.data || {}),
                        on_selected: function () {
                           
                            
                        },
                    })).open();
                    break;
                    
                case "btn_chon_nghiep_vu_va_hoat_dong":
                    return new dialogs.SelectParamsDialog(this, _.extend({}, this.nodeOptions, {
                        res_model: 'tong.hop.bctc.chon.nghiep.vu.va.hoat.dong.lctt.form',
                        title: 'Chọn chứng từ vào các hoạt động lưu chuyển tiền tệ',
                        ref_views: [['tong_hop.view_tong_hop_bctc_chon_nghiep_vu_va_hoat_dong_lctt_form_tham_so_form', 'form']],
                        // context: _.extend(event.data.record.context || {}, event.data.record.data || {}),
                        on_selected: function () {
                           
                            
                        },
                    })).open();
                    break;

                case "btn_them_phu_luc":
                    return new dialogs.FormViewDialog(this, _.extend({}, this.nodeOptions, {
                        model: this.model,
                        //parentID: data.parentID,
                        readonly: this.mode == "readonly",
                        recordID: this.handle,
                        res_model: this.modelName,
                        shouldSaveLocally: true,
                        disable_multiple_selection: true,
                        title: 'Thêm phụ lục',
                        ref_views: [['tong_hop.view_tong_hop_bctc_them_phu_luc_form_tham_so_form', 'form']],
                        // context: _.extend(event.data.record.context || {}, event.data.record.data || {}),
                        on_selected: function () {
                           
                            
                        },
                    })).open();
                    break;

                
                case "btn_thiet_lap_ct":
                    var ma_bao_cao = 'B01-DN';
                    var danh_sach_bc = ['B01-DN','B02-DN','B03-DN','B03-DN-GT'];
                    for(var i=0; i<danh_sach_bc.length; i++) {
                        var item = danh_sach_bc[i];
                        var $page = $('li.' + item);
                        if ($page.length == 1 && $page.hasClass('active')) {
                            ma_bao_cao = item;
                            break;
                        }
                    };
                    this.rpc_action({
                        model: 'tien.ich.thiet.lap.bao.cao.tai.chinh',
                        method: 'thuc_hien_lay_bao_cao_theo_ma_bao_cao',
                        args: {'ma_bao_cao':ma_bao_cao },
                        callback: function(result) {                            
                            new dialogs.FormViewDialog(self, _.extend({}, self.nodeOptions, {
                                model: self.model,
                                //parentID: data.parentID,
                                readonly: self.mode == "readonly",
                                res_id: result,
                                res_model:'tien.ich.thiet.lap.bao.cao.tai.chinh' ,
                                shouldSaveLocally: true,
                                disable_multiple_selection: true,
                                title: 'Thiết lập báo cáo tài chính',
                                ref_views: [['tien_ich.view_tien_ich_thiet_lap_bao_cao_tai_chinh_form', 'form']],
                                // context: _.extend(event.data.record.context || {}, event.data.record.data || {}),
                                on_selected: function () {


                                },
                            })).open();
                            }
                    });
                    
                    break;
                
               
            }
            
        },


      

       
    });
    
    var BaoCaoTaiChinhView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: BaoCaoTaiChinhController,
        }),
    });
    
    view_registry.add('tong_hop_bao_cao_tai_chinh_view', BaoCaoTaiChinhView);
    
    return BaoCaoTaiChinhView;
});

odoo.define('tong_hop.tong_hop_bao_cao_tai_chinh_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var BaoCaoTaiChinhController = ListController.extend({
        _onCreate: function() {
            var self = this;
            new dialogs.FormParamsDialog(this, _.extend({}, this.nodeOptions, {
                res_model: 'tong.hop.lap.bao.cao.tai.chinh',
                title: 'Chọn tham số báo cáo:Báo cáo tài chính',
                ref_views: [['tong_hop.view_tong_hop_bao_cao_tai_chinh_form', 'form']],
                on_selected: function (params,handle) {
                   
                    var context = {
                        'default_KY': params.KY,
                        'default_NAM': params.NAM,
                        'default_DOANH_NGHIEP_SELECTION': params.DOANH_NGHIEP_SELECTION,
                        'default_TU': params.TU,
                        'default_DEN': params.DEN,
                    };
                    var default_chi_tiet = [];
                    // Lấy data hiện tại của form
                    //var current_data = event.data.record.data;
                    // Lấy data của chứng từ chi tiết
                    var chi_tiet_ids = params.TONG_HOP_LAP_BAO_CAO_TAI_CHINH_CHI_TIET_IDS;
                    for (var i=0; i< chi_tiet_ids.length; i++) {
                        var chi_tiet = chi_tiet_ids[i];
                    
                            default_chi_tiet.push( {
                                'AUTO_SELECT': chi_tiet.AUTO_SELECT,
                                'MA_BAO_CAO_ID': chi_tiet.MA_BAO_CAO_ID,
                                'MA_PHU_LUC_ID': chi_tiet.MA_BAO_CAO_ID,
                                'TEN_PHU_LUC': chi_tiet.TEN_BAO_CAO,

                            });
                        
                        
                    }
                    context['default_LAY_DU_LIEU_THAM_SO'] = default_chi_tiet;

                    self.createRecord(context);
                    self.closeDialog(handle);
                   
                },
            })).open();
            
        },
    });
    
    var BaoCaoTaiChinhView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: BaoCaoTaiChinhController,
        }),
    });
    
    view_registry.add('tong_hop_bao_cao_tai_chinh_list_view', BaoCaoTaiChinhView);
    
    return BaoCaoTaiChinhView;

});
