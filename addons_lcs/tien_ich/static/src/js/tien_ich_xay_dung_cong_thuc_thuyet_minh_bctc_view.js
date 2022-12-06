odoo.define('tien_ich.xay_dung_cong_thuc_thuyet_minh_bctc_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var XayDungCongThucController = FormController.extend({
        onViewLoaded: function(e, defer) {
            // them moi
            // this.model.context = _.extend({}, this.model.context || {}, {'default_COT': e.colName});
            
            // this.setContext({'default_COT': e.colName});
            // var fieldWidget = this.getFieldWidget('TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_LOAI_CHI_TIEU_CHI_TIET_IDS');
            // fieldWidget.do_filter(['COT', e.colName]);
            if (defer) {
                defer.resolve();
            }
        },
        _onButtonClicked: function(event) {
            event.stopPropagation();
            var self = this;
            switch (event.data.attrs.id)
            {
                
                case "btn_xoa_cong_thuc_tmbctc":
                    // self.changeFieldValue('STEP', 2);
                    this.rpc_action({
                        model: 'tien.ich.thuyet.minh.bao.cao.tai.chinh.chi.tiet',
                        method: 'thuc_hien_xoa_cong_thuc_tmbctc',
                        // args: {},
                        callback: function(result) {
                            self.updateUI(result);
                        }
                    })
                    break;
                case "btn_lay_lai_cong_thuc_mac_dinh_tmbctc":
                    this.rpc_action({
                        model: 'tien.ich.thuyet.minh.bao.cao.tai.chinh.chi.tiet',
                        method: 'thuc_hien_lay_gia_tri_mac_dinh_tmbctc',
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
            if (field=='TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_LOAI_CHI_TIEU_TONG_HOP_IDS'){
                var gia_tri_details = this.getFieldValue('TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_LOAI_CHI_TIEU_TONG_HOP_IDS');
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
                self.updateUI({'CUOI_NAM':gia_tri_sau_khi_thay_doi_o_details});
            }
            else if (field=='TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_LOAI_CHI_TIEU_CHI_TIET_IDS'){
                    var gia_tri_details = this.getFieldValue('TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_LOAI_CHI_TIEU_CHI_TIET_IDS');
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
                self.updateUI({'CUOI_NAM':gia_tri_sau_khi_thay_doi_o_details});
               
                }
        
        },
    });

    
    var XayDungCongThucControllerView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: XayDungCongThucController,
        }),
    });
    
    view_registry.add('xay_dung_cong_thuc_thuyet_minh_bctc_form_view', XayDungCongThucControllerView);
    
    return XayDungCongThucControllerView;
});
