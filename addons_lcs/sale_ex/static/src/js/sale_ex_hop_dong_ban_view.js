odoo.define('sale_ex.sale_ex_hop_dong_ban_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var HopDongBanController = FormController.extend({

        _onButtonClicked: function(event) {
            var self = this;
			event.stopPropagation();
            switch (event.data.attrs.id)
            {
                case "btn_chon_chung_tu_chi":
                   return new dialogs.SelectParamsDialog(this, _.extend({}, this.nodeOptions, {
                        res_model: 'sale.ex.hop.dong.ban.chon.chung.tu.chi.form',
                        title: 'Chọn chứng từ chi',
                        ref_views: [['sale_ex.view_sale_ex_hop_dong_ban_chon_chung_tu_chi_form_tham_so_form', 'form']],
                        // context: _.extend(event.data.record.context || {}, event.data.record.data || {}),
                        on_selected: function (records) {
                           
                        }, 
                    })).open();
					break;
                
                case "btn_chon_chung_tu_thu":
                    return new dialogs.SelectParamsDialog(this, _.extend({}, this.nodeOptions, {
                         res_model: 'sale.ex.hop.dong.ban.chon.chung.tu.thu.form',
                         title: 'Chọn chứng từ thu',
                         ref_views: [['sale_ex.view_sale_ex_hop_dong_ban_chon_chung_tu_thu_form_tham_so_form', 'form']],
                         // context: _.extend(event.data.record.context || {}, event.data.record.data || {}),
                         on_selected: function (records) {
                            
                         }, 
                     })).open();
					 break;

                    // case "btn_de_nghi_ghi_doanh_so":
                    //  return new dialogs.SelectParamsDialog(this, _.extend({}, this.nodeOptions, {
                    //       res_model: 'sale.ex.hop.dong.ban.de.nghi.ghi.doanh.so.form',
                    //       title: 'Đề nghị ghi doanh số',
                    //       ref_views: [['sale_ex.view_sale_ex_hop_dong_ban_de_nghi_ghi_doanh_so_form_tham_so_form', 'form']],
                    //       // context: _.extend(event.data.record.context || {}, event.data.record.data || {}),
                    //       on_selected: function (params) {
                    //           var context={
                    //               'default_GIA_TRI_THANH_LY':params.GTTL_QUY_DOI,
                    //           }
                    //           var default_chi_tiet =[]
                    //           var chi_tiet_ids =params.SALE_EX_HOP_DONG_BAN_CHI_TIET_GHI_NHAN_DOANH_SO_IDS;
                    //           for(var i=0;i<chi_tiet_ids.length;i++){
                    //               var chi_tiet = chi_tiet_ids[i];
                    //                 default_chi_tiet.push((0,0,{
                    //                     'NHAN_VIEN_ID' : chi_tiet.NHAN_VIEN_ID,
                    //                     'DON_VI':chi_tiet.DON_VI,
                    //                     'HANG_HOA_ID':chi_tiet.HANG_HOA_ID,
                    //                     'TY_LE_PT':chi_tiet.TY_LE_PHAN_TRAM,
                    //                     'DOANH_SO_GHI_NHAN':chi_tiet.DOANH_SO_GHI_NHAN_HUY_BO,
                    //                     'DIEN_GIAI':chi_tiet.DIEN_GIAI,

                    //                 }))
                    //           }
                             
                    //           context['default_LAY_CHI_TIET_GHI_NHAN_DOANH_SO']=default_chi_tiet;
                    //           self.createRecord(context);

                    //       }, 
                    //   })).open();
                
                default: 
                   this._super.apply(this, arguments);
            }
            
        }
    });
    
    var HopDongBanView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: HopDongBanController,
        }),
    });
    
    view_registry.add('sale_ex_hop_dong_ban_view', HopDongBanView);
    
    return HopDongBanView;
});
