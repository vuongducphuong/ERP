odoo.define('tong_hop.tong_hop_bctc_chon_nghiep_vu_va_hoat_dong_lctt_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var BCTCChonChungTuVaHDLCTTController = FormController.extend({
        
        _onButtonClicked: function(event) {
            var self = this;
			event.stopPropagation();
            switch (event.data.attrs.id)
            {
                
                case "btn_tiep_theo":
                    var step=this.getFieldValue('STEP');
                    
                    self.changeFieldValue('STEP', step+1);
                    // $('button[name="btn_tiep_theo"]');
                    break;

                case "btn_ve_truoc":
                    var step=this.getFieldValue('STEP');
                    self.changeFieldValue('STEP', step-1);
                    // $('button[name="btn_tiep_theo"]');
                    break;

                default: 
               this._super.apply(this, arguments);
                  
                
            }
            
        },
       
    });
    
    var BCTCChonChungTuVaHDLCTTView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: BCTCChonChungTuVaHDLCTTController,
        }),
    });
    
    view_registry.add('tong_hop_bctc_chon_nghiep_vu_va_hoat_dong_lctt_form_view', BCTCChonChungTuVaHDLCTTView);
    
    return BCTCChonChungTuVaHDLCTTView;
});

