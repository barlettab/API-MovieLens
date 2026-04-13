from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import os

app = FastAPI()

# Carregamento dos artefatos
try:
    path = "recomendador_movies_knn.sav"
    if not os.path.exists(path):
        path = r"C:\Users\Windows10\Desktop\API-movie-lens\recomendador_movies_knn.sav"
        
    artefatos = joblib.load(path)
    
    # Adicionando o user_movie que é necessário para a lógica de recomendação por usuário
    user_movie = artefatos["user_movie"] 
    movie_ids = artefatos["movie_ids"]
    movie_index = artefatos["movie_index"]
    id_to_title = artefatos["id_to_title"]
    distances_all = artefatos["distances_all"]
    indices_all = artefatos["indices_all"]
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")

class InputData(BaseModel):
    user_id: int = Field(..., ge=1) # Agora o campo correto é user_id
    top_k: int = Field(5, ge=1, le=20)

@app.post("/predict")
async def predict(data: InputData):
    try:
        uid = int(data.user_id) # Acessando o atributo correto
        
        # 1. Verifica se o usuário existe na matriz do modelo
        if uid not in user_movie.index:
            raise HTTPException(status_code=404, detail=f"Usuario {uid} nao encontrado")

        # 2. Busca os filmes que o usuário já assistiu
        filmes_assistidos = user_movie.loc[uid]
        filmes_assistidos_ids = filmes_assistidos[filmes_assistidos > 0].index.tolist()

        recomendacoes = {}

        # 3. Lógica de recomendação: busca vizinhos para cada filme assistido
        for filme_id in filmes_assistidos_ids:
            if filme_id in movie_index:
                idx = int(movie_index[filme_id])
                
                vizinhos = indices_all[idx]
                distancias = distances_all[idx]

                for i, dist in zip(vizinhos, distancias):
                    m_id = int(movie_ids[i])
                    
                    # Não recomendar o que ele já viu
                    if m_id in filmes_assistidos_ids:
                        continue

                    if m_id not in recomendacoes:
                        recomendacoes[m_id] = 0
                    
                    # Acumula o score de similaridade
                    recomendacoes[m_id] += (1 - float(dist))

        # 4. Ordenação e formatação final
        top_recs = sorted(recomendacoes.items(), key=lambda x: x[1], reverse=True)[:data.top_k]

        final_recs = []
        for m_id, score in top_recs:
            final_recs.append({
                "movie_id": int(m_id),
                "title": str(id_to_title.get(m_id, "Desconhecido")),
                "relevance_score": round(float(score), 4)
            })

        return {
            "input_user_id": uid,
            "movies_watched_count": len(filmes_assistidos_ids),
            "recommendations": final_recs
        }
        
    except HTTPException as http_e:
        raise http_e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))