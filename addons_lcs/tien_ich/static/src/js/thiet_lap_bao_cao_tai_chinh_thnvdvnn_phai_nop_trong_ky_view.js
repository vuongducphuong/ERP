odoo.define('tien_ich.thiet_lap_bao_cao_tai_chinh_thnvdvnn_phai_nop_trong_ky_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormRenderer = require('web.FormRenderer');
    var BasicModel = require('web.BasicModel');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var ThietLapBaoCaoTaiChinhTHNVDVNNPhaiNopTrongKyController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
       
        _onButtonClicked: function(event) {
            var self = this;
			event.stopPropagation();
            switch (event.data.attrs.id)
            {
                
                case "btn_xoa_cong_thuc_1":
                    // self.changeFieldValue('STEP', 2);
                    this.rpc_action({
                        model: 'tien.ich.thuc.hien.nghia.vu.doi.voi.nha.nuoc.chi.tiet',
                        method: 'thuc_hien_xoa_cong_thuc_1',
                        // args: {},
                        callback: function(result) {
                            self.updateUI(result);
                        }
                    })
                    break;
                case "btn_lay_lai_cong_thuc_mac_dinh_1":
                    // self.changeFieldValue('STEP', 2);
                    this.rpc_action({
                        model: 'tien.ich.thuc.hien.nghia.vu.doi.voi.nha.nuoc.chi.tiet',
                        method: 'thuc_hien_lay_gia_tri_mac_dinh_phai_nop_trong_ky',
                        args: {'ten_bao_cao': self.params.ten_bao_cao, 'ma_chi_tieu':self.params.ma_chi_tieu },
                        callback: function(result) {
                            self.updateUI(result);
                        }
                    })
                    break;

                default: 
                   this._super.apply(this, arguments);
            }
            
        },

        onFieldChanged: function(field) {
            var self = this;
            
            var gia_tri_sau_khi_thay_doi_o_details ;
            if (field=='TIEN_ICH_TINH_HINH_THNVDVNN_PNTK_LOAI_CHI_TIEU_TONG_HOP_IDS'){
                var gia_tri_details = this.getFieldValue('TIEN_ICH_TINH_HINH_THNVDVNN_PNTK_LOAI_CHI_TIEU_TONG_HOP_IDS');
                var i;
                for (i = 0; i < gia_tri_details.length; i++){
                    var item = gia_tri_details[i];
                    var phep_tinh;
                    var ma_chi_tieu ;
                    if (item.MA_CHI_TIEU==null){
                        ma_chi_tieu = '';
                    }
                    else{
                          ma_chi_tieu = item.MA_CHI_TIEU;
                    }

                    if (item.PHEP_TINH =='CONG'){
                        phep_tinh = '+';
                    }
                    else if (item.PHEP_TINH =='TRU'){
                         phep_tinh = '-' ;
                    }
                    if(i==0 && phep_tinh =='+' ){
                        gia_tri_sau_khi_thay_doi_o_details = '[' +  ma_chi_tieu + ']' ;
                    }else{
                        gia_tri_sau_khi_thay_doi_o_details += phep_tinh + '[' +  ma_chi_tieu + ']' ;
                    }
                }
            }
            else{
                var gia_tri_details = this.getFieldValue('TIEN_ICH_TINH_HINH_THNVDVNN_PNTK_LOAI_CHI_TIEU_CHI_TIET_IDS');
                var i;
                for (i = 0; i < gia_tri_details.length; i++){
                    var item = gia_tri_details[i];
                    var phep_tinh; 
                    var ky_hieu;
                    if (item.KY_HIEU==null){
                        ky_hieu = '';
                    }
                    else{
                          ky_hieu = item.KY_HIEU;
                    }

                    if (item.PHEP_TINH =='CONG'){
                        phep_tinh = '+';
                    }
                    else if (item.PHEP_TINH =='TRU'){
                         phep_tinh = '-' ;
                    }
                    var string_all_tai_khoan;
                    var tai_khoan;
                    var tai_khoan_du;
                    if (item.TAI_KHOAN_ID.display_name !=null && item.TK_DOI_UNG_ID.display_name !=null){
                        tai_khoan = item.TAI_KHOAN_ID.display_name; 
                        tai_khoan_du = item.TK_DOI_UNG_ID.display_name; 
                        string_all_tai_khoan = tai_khoan+'/'+tai_khoan_du ;
                    }
                    else{
                        if (item.TAI_KHOAN_ID.display_name !=null && item.TK_DOI_UNG_ID.display_name == null){
                            string_all_tai_khoan = item.TAI_KHOAN_ID.display_name; 
                        }
                        else {
                            string_all_tai_khoan = '';
                        }
                    }
                    if(i==0 && phep_tinh =='+' ){
                        gia_tri_sau_khi_thay_doi_o_details = ky_hieu +'('+string_all_tai_khoan+')';
                    }else{
                        gia_tri_sau_khi_thay_doi_o_details += phep_tinh + ky_hieu +'('+string_all_tai_khoan+')' ;
                    }

                }
            //self.changeFieldValue('CONG_THUC',gia_tri_sau_khi_thay_doi_o_details);
            self.updateUI({'SO_PHAI_NOP_TRONG_KY':gia_tri_sau_khi_thay_doi_o_details});
            
        }
    },
       
    });

    var ThietLapBaoCaoTaiChinhTHNVDVNNPhaiNopTrongKyRenderer = FormRenderer.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });

    var ThietLapBaoCaoTaiChinhTHNVDVNNPhaiNopTrongKyModel = BasicModel.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });
    
    var ThietLapBaoCaoTaiChinhTHNVDVNNPhaiNopTrongKyView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Model: ThietLapBaoCaoTaiChinhTHNVDVNNPhaiNopTrongKyModel,
            Renderer: ThietLapBaoCaoTaiChinhTHNVDVNNPhaiNopTrongKyRenderer,
            Controller: ThietLapBaoCaoTaiChinhTHNVDVNNPhaiNopTrongKyController,
        }),
    });
    
    view_registry.add('thiet_lap_bao_cao_tai_chinh_thnvdvnn_phai_nop_trong_ky_view', ThietLapBaoCaoTaiChinhTHNVDVNNPhaiNopTrongKyView);
    
    return ThietLapBaoCaoTaiChinhTHNVDVNNPhaiNopTrongKyView;
});
