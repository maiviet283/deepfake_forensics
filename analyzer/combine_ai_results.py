def combine_ai_results(isItAi_decopy, isItAi_wasit, probability_decopy, probability_waist):
    # Nếu chỉ có wasitai
    if isItAi_decopy is None or probability_decopy is None:
        return {
            'isItAi': isItAi_wasit,
            'probability': round(probability_waist, 2)
        }

    # Nếu chỉ có decopy
    if isItAi_wasit is None or probability_waist is None:
        return {
            'isItAi': isItAi_decopy,
            'probability': round(probability_decopy, 2)
        }

    # Nếu cả hai đều có
    if isItAi_decopy == isItAi_wasit:
        return ({
            'isItAi': isItAi_wasit,
            'probability': round(probability_decopy*0.4 + probability_waist*0.6, 2)
        })
    else:
        if probability_decopy * 0.4 < probability_waist * 0.6:
            return ({
                'isItAi': isItAi_wasit,
                'probability': round(probability_waist * 0.6 - probability_decopy * 0.4, 2)
            })
        elif probability_decopy * 0.4 > probability_waist * 0.6:
            return ({
                'isItAi': isItAi_decopy,
                'probability': round(probability_decopy * 0.4 - probability_waist * 0.6, 2)
            })
        else:
            return ({
                'isItAi': 'Chưa Xác Định',
                'probability': '50'
            })
