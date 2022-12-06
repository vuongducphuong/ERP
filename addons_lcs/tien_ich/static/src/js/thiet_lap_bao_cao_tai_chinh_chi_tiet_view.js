odoo.define('tien_ich.thiet_lap_bao_cao_tai_chinh_chi_tiet_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormRenderer = require('web.FormRenderer');
    var BasicModel = require('web.BasicModel');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var ThietLapBaoCaoTaiChinhChiTietController = FormController.extend({
        custom_events: _.extend({}, FormController.prototype.custom_events, {
            request_data_for_many2one: '_onRespondRequest',
        }),

        _onRespondRequest: function (ev) {
            ev.stopPropagation();
            ev.data.callback(this.data_for_many2one);
        },

        init: function () {
            this._super.apply(this, arguments);
        },

        onViewLoaded(e, defer) {
            this.data_for_many2one = e.data_for_many2one;
            if (defer) {
                defer.resolve();
            }
        },
       
        _onButtonClicked: function(event) {
            event.stopPropagation();
            var self = this;
            switch (event.data.attrs.id)
            {
                
                case "btn_xoa_cong_thuc":
                    // self.changeFieldValue('STEP', 2);
                    this.rpc_action({
                        model: 'tien.ich.bao.cao.tai.chinh.chi.tiet',
                        method: 'thuc_hien_xoa_cong_thuc',
                        // args: {},
                        callback: function(result) {
                            self.updateUI(result);
                        }
                    })
                    break;
                case "btn_lay_lai_cong_thuc_mac_dinh":
                    this.rpc_action({
                        model: 'tien.ich.bao.cao.tai.chinh.chi.tiet',
                        method: 'thuc_hien_lay_gia_tri_mac_dinh',
                        args: {'ten_bao_cao': self.params.ten_bao_cao, 'ma_chi_tieu':self.params.ma_chi_tieu },
                        callback: function(result) {
                            self.updateUI(result);
                        }
                    })
                    break;

                default: 
                   this._super.apply(this, arguments);
                   break;
            }
            
        },

        onFieldChanged: function(field) {
            var self = this;
            
            var gia_tri_sau_khi_thay_doi_o_details ;
            if (field=='TIEN_ICH_XAY_DUNG_CONG_THUC_LOAI_CHI_TIEU_TONG_HOP_IDS'){
                var gia_tri_details = this.getFieldValue('TIEN_ICH_XAY_DUNG_CONG_THUC_LOAI_CHI_TIEU_TONG_HOP_IDS');
                var i;
                for (i = 0; i < gia_tri_details.length; i++){
                    var item = gia_tri_details[i];
                    var phep_tinh;
                    var ma_chi_tieu ;
                    if (!item.MA_CHI_TIEU){
                        ma_chi_tieu = '';
                    }
                    else {
                          ma_chi_tieu = item.MA_CHI_TIEU.includes('_,_') ? item.MA_CHI_TIEU.split('_,_')[1] : item.MA_CHI_TIEU;
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
                self.updateUI({'CONG_THUC':gia_tri_sau_khi_thay_doi_o_details});
            }
            else if (field=='TIEN_ICH_XAY_DUNG_CONG_THUC_LOAI_CHI_TIEU_CHI_TIET_IDS'){
                    var gia_tri_details = this.getFieldValue('TIEN_ICH_XAY_DUNG_CONG_THUC_LOAI_CHI_TIEU_CHI_TIET_IDS');
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
                        if (item.TAI_KHOAN_ID !=null && item.TK_DOI_UNG_ID !=null){
                            tai_khoan = item.TAI_KHOAN_ID.SO_TAI_KHOAN; 
                            tai_khoan_du = item.TK_DOI_UNG_ID.SO_TAI_KHOAN; 
                            string_all_tai_khoan = tai_khoan+'/'+tai_khoan_du ;
                        }
                        else{
                            if (item.TAI_KHOAN_ID !=null && item.TK_DOI_UNG_ID == null){
                                string_all_tai_khoan = item.TAI_KHOAN_ID.SO_TAI_KHOAN; 
                            }
                            else {
                                string_all_tai_khoan = '';
                            }
                        }
                        if(i==0 && phep_tinh =='+' ){
                            gia_tri_sau_khi_thay_doi_o_details = ky_hieu +'('+string_all_tai_khoan+')';
                        }else{
                            gia_tri_sau_khi_thay_doi_o_details += ky_hieu +'('+string_all_tai_khoan+')' ;
                        }

                        
    
                }
                self.updateUI({'CONG_THUC':gia_tri_sau_khi_thay_doi_o_details});
               
                }
        
        },
       
    });

    var ThietLapBaoCaoTaiChinhChiTietRenderer = FormRenderer.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });

    var ThietLapBaoCaoTaiChinhChiTietModel = BasicModel.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });
    
    var ThietLapBaoCaoTaiChinhChiTietView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Model: ThietLapBaoCaoTaiChinhChiTietModel,
            Renderer: ThietLapBaoCaoTaiChinhChiTietRenderer,
            Controller: ThietLapBaoCaoTaiChinhChiTietController,
        }),
    });
    
    view_registry.add('thiet_lap_bao_cao_tai_chinh_chi_tiet_view', ThietLapBaoCaoTaiChinhChiTietView);
    
    return ThietLapBaoCaoTaiChinhChiTietView;
});
