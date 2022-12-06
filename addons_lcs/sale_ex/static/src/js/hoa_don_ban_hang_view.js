odoo.define('sale_ex.hoa_don_ban_hang_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var HoaDonBanHangController = FormController.extend({
        onViewLoaded: function(e, defer) {
            var def = defer;
            var self = this;
            var loai_ban_hang = this.getFieldValue('HOA_DON');
            var nghiep_vu = '';
            if (loai_ban_hang =='BAN_HANG_HOA_DICH_VU_TRONG_NUOC'){
                nghiep_vu = 'TRONG_NUOC';
            }
            else if (loai_ban_hang =='BAN_HANG_XUAT_KHAU'){
                nghiep_vu = 'XUAT_KHAU';
            }
            else if (loai_ban_hang =='BAN_HANG_DAI_LY_BAN_DUNG_GIA'){
                nghiep_vu = 'DAI_LY';
            }
            else if (loai_ban_hang =='BAN_HANG_UY_THAC_XUAT_KHAU'){
                nghiep_vu = 'UY_THAC';
            }
            self.getFieldWidget('SALE_DOCUMENT_IDS').changeDomain([['LOAI_NGHIEP_VU','=',nghiep_vu]]);
            if (def) {
                def.resolve();
            }
        },
        onFieldChanged: function(field){
            if(['HOA_DON','DOI_TUONG_ID','SALE_DOCUMENT_IDS'].indexOf(field)>-1){
                var loai_ban_hang = this.getFieldValue('HOA_DON');
                var nghiep_vu = '';
                if (loai_ban_hang =='BAN_HANG_HOA_DICH_VU_TRONG_NUOC'){
                    nghiep_vu = 'TRONG_NUOC';
                }
                else if (loai_ban_hang =='BAN_HANG_XUAT_KHAU'){
                    nghiep_vu = 'XUAT_KHAU';
                }
                else if (loai_ban_hang =='BAN_HANG_DAI_LY_BAN_DUNG_GIA'){
                    nghiep_vu = 'DAI_LY';
                }
                else if (loai_ban_hang =='BAN_HANG_UY_THAC_XUAT_KHAU'){
                    nghiep_vu = 'UY_THAC';
                }
                var domain = [['LOAI_NGHIEP_VU','=',nghiep_vu]]
                var doi_tuong = this.getFieldValue('DOI_TUONG_ID');
                if (doi_tuong.id) {
                    domain.push(['DOI_TUONG_ID', '=', doi_tuong.id])
                }
                this.getFieldWidget('SALE_DOCUMENT_IDS').changeDomain(domain);
            } 
            // if(field == 'CHUNG_TU_BAN_HANG'){
            //     var CHUNG_TU_BAN_HANG = this.getFieldValue('CHUNG_TU_BAN_HANG')
            //     var id_ctbh;
            //     var name_ctbh;
            //     if (CHUNG_TU_BAN_HANG){
            //         id_ctbh =  CHUNG_TU_BAN_HANG.id;
            //         name_ctbh = CHUNG_TU_BAN_HANG.display_name;
            //     }
            //     this.rpc_action({
            //         model: 'sale.ex.hoa.don.ban.hang',
            //         method: 'lay_du_lieu_chung_tu_ban_hang',
            //         args: {
            //             'chung_tu_ban_hang_id' :id_ctbh,
            //             'chung_tu_ban_hang_name' : name_ctbh,
            //         },
            //         callback: function(result) {
            //             if (result) {
            //                 self.updateUI(result);
            //             }
            //         }
            //     });
            // }
            
        }
    });
    
    var HoaDonBanHangView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: HoaDonBanHangController,
        }),
    });
    
    view_registry.add('hoa_don_ban_hang_form_view', HoaDonBanHangView);
    
    return HoaDonBanHangView;
});