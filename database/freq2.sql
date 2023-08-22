create or replace view freq2 as
        select vacctype, symptom, freq_1 as frequency
        from freq1 
        union all
        select vacctype, symptom, freq_2 as frequency
        from freq1 
        union all
        select vacctype, symptom, freq_3 as frequency
        from freq1;